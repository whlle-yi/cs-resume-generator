"""FastAPI 依赖注入：从 app.state 取单例服务。"""

from __future__ import annotations

from fastapi import Request

from app.services.pdf_service import PdfService
from app.services.render_service import RenderService


def get_render_service(request: Request) -> RenderService:
    return request.app.state.render_service


def get_pdf_service(request: Request) -> PdfService:
    return request.app.state.pdf_service
