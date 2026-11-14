"""Jinja2 渲染服务：把 ResumeData 渲染成自包含 HTML。

模板与打印 CSS 位于 app/templates/，渲染产物内联全部样式，
无需任何外部资源请求，可直接用于 iframe 预览与 PDF 导出。
"""

from __future__ import annotations

import re
from functools import cache
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from app.core.errors import TemplateNotFoundError
from app.schemas.resume import ResumeData, SkillItem

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

# 模板注册表：新增模板时在此登记，同时提供 templates/<id>.html.j2 与 <id>.css
AVAILABLE_TEMPLATES: list[dict[str, str]] = [
    {
        "id": "classic",
        "name": "经典单栏",
        "description": "传统单栏版式，信息密度高，适合大多数企业投递场景",
    },
    {
        "id": "modern",
        "name": "简约双栏",
        "description": "左侧信息栏 + 右侧主栏，视觉层次清晰，适合互联网公司",
    },
]
TEMPLATE_IDS = {t["id"] for t in AVAILABLE_TEMPLATES}

_MONTH_FMT_RE = re.compile(r"^(\d{4})-(\d{2})$")


def _fmt_period(value: str) -> str:
    """把 2022-09 显示为 2022.09；「至今」原样输出。"""
    match = _MONTH_FMT_RE.match(value.strip())
    return f"{match.group(1)}.{match.group(2)}" if match else value


def _fmt_month(value: str) -> str:
    return _fmt_period(value)


def _join_skill_items(items: list[SkillItem]) -> str:
    """技能条目合并为「C/C++（熟练）、Python（熟练）」形式。"""
    return "、".join(f"{item.name}（{item.level}）" if item.level else item.name for item in items)


class RenderService:
    """模板渲染服务，可独立实例化（便于测试）。"""

    def __init__(self, templates_dir: Path | None = None) -> None:
        root = templates_dir or TEMPLATES_DIR
        self._env = Environment(
            loader=FileSystemLoader(str(root)),
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True,
            undefined=StrictUndefined,
        )
        self._env.filters["period"] = _fmt_period
        self._env.filters["month"] = _fmt_month
        self._env.filters["skill_items"] = _join_skill_items

    def render(self, data: ResumeData, template_id: str) -> str:
        """渲染简历为完整 HTML 文档。"""
        if template_id not in TEMPLATE_IDS:
            known = "、".join(sorted(TEMPLATE_IDS))
            raise TemplateNotFoundError(f"未知模板 {template_id!r}，可用模板：{known}")
        template = self._env.get_template(f"{template_id}.html.j2")
        return template.render(resume=data, css=self._get_css(template_id))

    @staticmethod
    @cache
    def _get_css(template_id: str) -> str:
        """合并公共样式与模板私有样式（结果缓存）。"""
        base = (TEMPLATES_DIR / "styles" / "base.css").read_text(encoding="utf-8")
        private = (TEMPLATES_DIR / "styles" / f"{template_id}.css").read_text(encoding="utf-8")
        return f"{base}\n{private}"


def get_available_templates() -> list[dict[str, Any]]:
    """返回模板注册表（副本，防止调用方误改）。"""
    return [t.copy() for t in AVAILABLE_TEMPLATES]
