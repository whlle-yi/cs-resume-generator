"""API 契约测试。"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


def test_health(client: TestClient):
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["version"]


def test_meta_templates(client: TestClient):
    resp = client.get("/api/v1/meta/templates")
    assert resp.status_code == 200
    ids = {t["id"] for t in resp.json()["templates"]}
    assert ids == {"classic", "modern"}


def test_resume_sample(client: TestClient):
    resp = client.get("/api/v1/resume/sample")
    assert resp.status_code == 200
    body = resp.json()
    assert body["schema_version"] == 1
    assert body["basics"]["name"]


def _render_payload(sample_data, template: str = "classic") -> dict:
    return {"data": sample_data.model_dump(mode="json"), "template": template}


def test_preview_returns_html(client: TestClient, sample_data):
    resp = client.post("/api/v1/resume/preview", json=_render_payload(sample_data))
    assert resp.status_code == 200
    html = resp.json()["html"]
    assert "陈晓东" in html
    assert "<!doctype html>" in html.lower()


def test_preview_modern_template(client: TestClient, sample_data):
    resp = client.post("/api/v1/resume/preview", json=_render_payload(sample_data, "modern"))
    assert resp.status_code == 200
    assert "sidebar" in resp.json()["html"]


def test_preview_unknown_template_returns_400(client: TestClient, sample_data):
    resp = client.post("/api/v1/resume/preview", json=_render_payload(sample_data, "nope"))
    assert resp.status_code == 400
    body = resp.json()
    assert body["code"] == "TEMPLATE_NOT_FOUND"


def test_preview_invalid_data_returns_422(client: TestClient):
    payload = {
        "data": {
            "basics": {
                "name": "",
                "objective": "后端开发",
                "phone": "abc",
                "email": "bad-email",
            }
        }
    }
    resp = client.post("/api/v1/resume/preview", json=payload)
    assert resp.status_code == 422
    body = resp.json()
    assert body["code"] == "VALIDATION_ERROR"
    assert body["details"]


@pytest.mark.pdf
def test_export_pdf(client: TestClient, sample_data):
    resp = client.post("/api/v1/resume/export/pdf", json=_render_payload(sample_data))
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/pdf"
    content = resp.content
    assert content.startswith(b"%PDF")
    assert len(content) > 10_000  # 正常单页 PDF 远大于 10KB


@pytest.mark.pdf
def test_export_pdf_filename_header(client: TestClient, sample_data):
    resp = client.post("/api/v1/resume/export/pdf", json=_render_payload(sample_data))
    disposition = resp.headers.get("content-disposition", "")
    assert "filename*=UTF-8''" in disposition
