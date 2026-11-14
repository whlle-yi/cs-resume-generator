"""简历核心接口：示例数据、HTML 预览、PDF 导出。"""

from __future__ import annotations

from urllib.parse import quote

from fastapi import APIRouter, Depends, Response

from app.api.deps import get_pdf_service, get_render_service
from app.schemas.resume import RenderRequest, ResumeData
from app.services.pdf_service import PdfService
from app.services.render_service import RenderService
from app.services.sample_service import load_sample_resume

router = APIRouter(tags=["resume"])


@router.get("/resume/sample", response_model=ResumeData, summary="示例简历数据")
async def get_sample() -> ResumeData:
    return load_sample_resume()


@router.post("/resume/preview", summary="渲染 HTML 预览")
async def preview(
    payload: RenderRequest,
    render_service: RenderService = Depends(get_render_service),
) -> dict[str, str]:
    html = render_service.render(payload.data, payload.template)
    return {"html": html}


@router.post("/resume/export/pdf", summary="导出 PDF 文件")
async def export_pdf(
    payload: RenderRequest,
    render_service: RenderService = Depends(get_render_service),
    pdf_service: PdfService = Depends(get_pdf_service),
) -> Response:
    html = render_service.render(payload.data, payload.template)
    pdf_bytes = await pdf_service.html_to_pdf(html)

    filename = quote(f"{payload.data.basics.name}_简历.pdf")
    headers = {"Content-Disposition": f"attachment; filename*=UTF-8''{filename}"}
    return Response(content=pdf_bytes, media_type="application/pdf", headers=headers)
