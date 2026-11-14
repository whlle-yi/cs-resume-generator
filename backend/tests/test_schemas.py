"""数据模型校验测试。"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.schemas.resume import (
    Award,
    Basics,
    Education,
    InternshipExperience,
    ProjectExperience,
    ResumeData,
    SkillGroup,
    SkillItem,
)


def test_sample_data_is_valid(sample_data):
    assert sample_data.basics.name == "陈晓东"
    assert len(sample_data.education) == 1
    assert len(sample_data.projects) == 2
    assert sample_data.schema_version == 1


def test_valid_minimal_resume():
    data = ResumeData(
        basics={
            "name": "张三",
            "objective": "后端开发工程师",
            "phone": "13800138000",
            "email": "zhangsan@example.com",
        }
    )
    assert data.education == []
    assert data.projects == []


def test_invalid_phone_rejected():
    with pytest.raises(ValidationError, match="手机号"):
        Basics(
            name="张三",
            objective="后端开发",
            phone="12345",
            email="zhangsan@example.com",
        )


def test_invalid_email_rejected():
    with pytest.raises(ValidationError):
        Basics(
            name="张三",
            objective="后端开发",
            phone="13800138000",
            email="not-an-email",
        )


def test_invalid_url_rejected():
    with pytest.raises(ValidationError, match="GitHub"):
        Basics(
            name="张三",
            objective="后端开发",
            phone="13800138000",
            email="zhangsan@example.com",
            github="github.com/no-scheme",
        )


def test_education_month_format_rejected():
    with pytest.raises(ValidationError, match="开始时间"):
        Education(
            school="某大学",
            major="计算机科学与技术",
            degree="本科",
            start_date="2022/09",
            end_date="2026-06",
        )


def test_education_date_order_rejected():
    with pytest.raises(ValidationError, match="结束时间不能早于开始时间"):
        Education(
            school="某大学",
            major="计算机科学与技术",
            degree="本科",
            start_date="2023-09",
            end_date="2022-06",
        )


def test_education_end_now_allowed():
    edu = Education(
        school="某大学",
        major="计算机科学与技术",
        degree="硕士",
        start_date="2022-09",
        end_date="至今",
    )
    assert edu.end_date == "至今"


def test_project_empty_highlights_rejected():
    with pytest.raises(ValidationError, match="项目要点"):
        ProjectExperience(
            name="项目",
            start_date="2024-01",
            end_date="2024-06",
            highlights=["   "],
        )


def test_internship_empty_highlights_rejected():
    with pytest.raises(ValidationError, match="实习要点"):
        InternshipExperience(
            company="某公司",
            position="开发实习生",
            start_date="2024-01",
            end_date="2024-06",
            highlights=[],
        )


def test_skill_level_literal_rejected():
    with pytest.raises(ValidationError):
        SkillItem(name="Python", level="天下无敌")


def test_skill_group_requires_items():
    with pytest.raises(ValidationError):
        SkillGroup(category="编程语言", items=[])


def test_award_month_format_rejected():
    with pytest.raises(ValidationError, match="获奖时间"):
        Award(name="奖学金", date="2024年12月")


def test_phone_email_whitespace_stripped():
    basics = Basics(
        name=" 张三 ",
        objective="后端开发",
        phone=" 13800138000 ",
        email=" zhangsan@example.com ",
    )
    assert basics.name == "张三"
    assert basics.phone == "13800138000"
