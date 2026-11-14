"""模板渲染服务测试。"""

from __future__ import annotations

import pytest

from app.core.errors import TemplateNotFoundError
from app.schemas.resume import ResumeData
from app.services.render_service import RenderService, get_available_templates


@pytest.fixture
def render_service() -> RenderService:
    return RenderService()


def _minimal_resume(name: str = "张三") -> ResumeData:
    return ResumeData(
        basics={
            "name": name,
            "objective": "后端开发工程师",
            "phone": "13800138000",
            "email": "zhangsan@example.com",
        }
    )


@pytest.mark.parametrize("template_id", ["classic", "modern"])
def test_render_sample_contains_sections(render_service, sample_data, template_id):
    html = render_service.render(sample_data, template_id)
    expected = ["陈晓东", "教育背景", "专业技能", "实习经历", "项目经历", "获奖情况", "自我评价"]
    for text in expected:
        assert text in html, f"渲染产物缺少「{text}」"
    assert "<style>" in html and "</style>" in html
    assert "2022.09 – 2026.06" in html


def test_render_escapes_user_input(render_service):
    data = _minimal_resume(name='<script>alert("xss")</script>')
    html = render_service.render(data, "classic")
    assert "<script>alert" not in html
    assert "&lt;script&gt;" in html


def test_render_unknown_template_raises(render_service):
    with pytest.raises(TemplateNotFoundError, match="未知模板"):
        render_service.render(_minimal_resume(), "not-exist")


def test_available_templates_registry():
    templates = get_available_templates()
    assert {t["id"] for t in templates} == {"classic", "modern"}
    # 返回副本，修改不影响注册表
    templates[0]["id"] = "hacked"
    assert get_available_templates()[0]["id"] == "classic"


def test_css_is_inlined_and_self_contained(render_service, sample_data):
    html = render_service.render(sample_data, "modern")
    assert "font-family" in html  # 公共样式已内联
    assert "--accent" in html  # 模板私有样式已内联
    assert "href=" not in html.split("<body")[0]  # head 中无外部资源引用
