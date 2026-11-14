"""业务异常体系：由 main.py 的全局异常处理器转换为统一 JSON 错误结构。"""

from __future__ import annotations


class AppError(Exception):
    """业务异常基类。"""

    status_code = 400
    code = "APP_ERROR"
    default_message = "请求处理失败"

    def __init__(self, message: str | None = None, *, details: object | None = None) -> None:
        self.message = message or self.default_message
        self.details = details
        super().__init__(self.message)


class TemplateNotFoundError(AppError):
    status_code = 400
    code = "TEMPLATE_NOT_FOUND"
    default_message = "简历模板不存在"


class RenderError(AppError):
    status_code = 500
    code = "RENDER_ERROR"
    default_message = "简历渲染失败"


class PdfEngineError(AppError):
    status_code = 500
    code = "PDF_ENGINE_ERROR"
    default_message = "PDF 导出失败，请稍后重试"
