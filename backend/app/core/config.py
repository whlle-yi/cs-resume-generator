"""全局配置：pydantic-settings 从环境变量 / .env 读取，统一带 RESUME_ 前缀。"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/app/core/config.py -> parents[3] 即仓库根目录
REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_FRONTEND_DIST = REPO_ROOT / "frontend" / "dist"


class Settings(BaseSettings):
    """应用配置项。"""

    model_config = SettingsConfigDict(
        env_prefix="RESUME_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    debug: bool = False
    log_level: str = "INFO"
    api_prefix: str = "/api/v1"
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    pdf_timeout_ms: int = 30000
    # 生产模式下托管前端构建产物；留 None 时自动探测仓库内 frontend/dist
    frontend_dist_dir: Path | None = None

    @property
    def resolved_frontend_dist(self) -> Path | None:
        """返回存在的前端产物目录，不存在则返回 None（纯 API 模式）。"""
        dist = self.frontend_dist_dir or DEFAULT_FRONTEND_DIST
        return dist if dist.is_dir() else None


@lru_cache
def get_settings() -> Settings:
    return Settings()
