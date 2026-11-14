"""健康检查。"""

from __future__ import annotations

from fastapi import APIRouter

from app import __version__

router = APIRouter(tags=["health"])


@router.get("/health", summary="健康检查")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "cs-resume-backend", "version": __version__}
