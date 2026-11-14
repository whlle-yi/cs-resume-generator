"""示例简历数据：供「填充示例」按钮与测试共用。"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from app.schemas.resume import ResumeData

SAMPLE_PATH = Path(__file__).resolve().parent.parent / "data" / "sample_resume.json"


@lru_cache(maxsize=1)
def _load_raw() -> str:
    return SAMPLE_PATH.read_text(encoding="utf-8")


def load_sample_resume() -> ResumeData:
    """每次返回全新实例，避免调用方相互影响。"""
    return ResumeData.model_validate_json(_load_raw())
