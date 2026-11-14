"""Playwright 无头 Chromium PDF 导出引擎。

浏览器实例惰性创建、常驻复用（首次导出约需数秒，之后毫秒级），
进程退出时由 FastAPI lifespan 统一释放。
"""

from __future__ import annotations

import asyncio
import contextlib
import logging

from playwright.async_api import Browser, Playwright, async_playwright

from app.core.errors import PdfEngineError

logger = logging.getLogger(__name__)


class PdfService:
    """把渲染好的自包含 HTML 转成 A4 PDF。"""

    def __init__(self, timeout_ms: int = 30000) -> None:
        self._timeout_ms = timeout_ms
        self._pw: Playwright | None = None
        self._browser: Browser | None = None
        self._lock = asyncio.Lock()

    async def html_to_pdf(self, html: str) -> bytes:
        browser = await self._ensure_browser()
        page = await browser.new_page()
        try:
            await page.set_content(html, wait_until="load", timeout=self._timeout_ms)
            # 等待系统字体（宋体 / Times New Roman）加载完成，避免 PDF 中字体回退
            await page.evaluate("() => document.fonts.ready")
            return await page.pdf(
                print_background=True,
                prefer_css_page_size=True,
            )
        except Exception as exc:
            raise PdfEngineError(f"PDF 导出失败：{exc}") from exc
        finally:
            await page.close()

    async def _ensure_browser(self) -> Browser:
        async with self._lock:
            if self._browser is not None and self._browser.is_connected():
                return self._browser
            logger.info("正在启动 PDF 渲染引擎（无头 Chromium）...")
            try:
                self._pw = await async_playwright().start()
                self._browser = await self._pw.chromium.launch(headless=True)
            except Exception as exc:
                self._pw = None
                self._browser = None
                raise PdfEngineError(f"启动 PDF 渲染引擎失败：{exc}") from exc
            logger.info("PDF 渲染引擎就绪")
            return self._browser

    async def aclose(self) -> None:
        """释放浏览器资源（应用关闭时调用）。"""
        async with self._lock:
            if self._browser is not None:
                try:
                    await self._browser.close()
                except Exception:  # noqa: BLE001 关闭失败无需中断退出流程
                    logger.warning("关闭 Chromium 时出现异常（忽略）")
            if self._pw is not None:
                with contextlib.suppress(Exception):
                    await self._pw.stop()
            self._browser = None
            self._pw = None
