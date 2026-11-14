"""应用入口：应用工厂 + 统一异常处理 + 生产模式静态托管。

启动：
    开发模式（纯 API）:   uvicorn app.main:app --reload --port 8000
    生产模式（托管前端）: 先构建 frontend/，uvicorn app.main:app --port 8000
"""

from __future__ import annotations

import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app import __version__
from app.api.v1.router import api_router
from app.core.config import Settings, get_settings
from app.core.errors import AppError
from app.core.logging import setup_logging
from app.schemas.common import ErrorBody
from app.services.pdf_service import PdfService
from app.services.render_service import RenderService

logger = logging.getLogger(__name__)


def _error_response(
    code: str, message: str, details: object | None, status_code: int
) -> JSONResponse:
    body = ErrorBody(code=code, message=message, details=details)
    return JSONResponse(status_code=status_code, content=body.model_dump())


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # 应用退出时释放无头浏览器
    await app.state.pdf_service.aclose()


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    setup_logging(settings.log_level)

    app = FastAPI(
        title="CS 简历生成器 API",
        description="填写结构化信息，渲染计算机专业简历并导出 PDF",
        version=__version__,
        lifespan=lifespan,
    )
    app.state.settings = settings
    app.state.render_service = RenderService()
    app.state.pdf_service = PdfService(timeout_ms=settings.pdf_timeout_ms)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def access_log(request: Request, call_next):
        started = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - started) * 1000
        logger.info(
            "%s %s -> %s (%.0fms)",
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
        )
        return response

    @app.exception_handler(AppError)
    async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
        return _error_response(exc.code, exc.message, exc.details, exc.status_code)

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        # errors() 的 ctx 里含异常对象，不可直接 JSON 序列化，只保留可序列化字段
        details = [
            {"loc": list(err.get("loc", [])), "msg": err.get("msg"), "type": err.get("type")}
            for err in exc.errors()
        ]
        return _error_response("VALIDATION_ERROR", "请求数据校验失败", details, 422)

    @app.exception_handler(Exception)
    async def unhandled_error_handler(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("未处理异常：%s", exc)
        return _error_response("INTERNAL_ERROR", "服务器内部错误", None, 500)

    app.include_router(api_router, prefix=settings.api_prefix)

    # 生产模式：托管前端构建产物，单进程即可部署
    dist_dir = settings.resolved_frontend_dist
    if dist_dir is not None:
        app.mount("/", StaticFiles(directory=str(dist_dir), html=True), name="frontend")
        logger.info("已托管前端静态资源：%s", dist_dir)

    return app


app = create_app()
