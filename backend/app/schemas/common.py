"""通用 API 结构：统一错误响应体。"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class ErrorBody(BaseModel):
    """所有非 2xx 响应的统一结构。"""

    code: str
    message: str
    details: Any | None = None
