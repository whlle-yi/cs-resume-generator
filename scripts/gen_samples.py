"""生成两套模板的样例 PDF 到 output/ 目录，用于模板改动后的目检。

用法：
    cd backend
    .venv/Scripts/python ../scripts/gen_samples.py
"""

from __future__ import annotations

import asyncio
from pathlib import Path

from app.services.pdf_service import PdfService
from app.services.render_service import RenderService
from app.services.sample_service import load_sample_resume

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"


async def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    data = load_sample_resume()
    service = PdfService()
    for template_id in ("classic", "modern"):
        html = RenderService().render(data, template_id)
        pdf = await service.html_to_pdf(html)
        out = OUTPUT_DIR / f"sample_{template_id}.pdf"
        out.write_bytes(pdf)
        print(f"{out}  {len(pdf)} bytes")
    await service.aclose()


if __name__ == "__main__":
    asyncio.run(main())
