"""元信息：模板列表等。"""

from __future__ import annotations

from fastapi import APIRouter

from app.services.render_service import get_available_templates

router = APIRouter(tags=["meta"])


@router.get("/meta/templates", summary="可用简历模板列表")
async def list_templates() -> dict[str, list[dict[str, str]]]:
    return {"templates": get_available_templates()}
