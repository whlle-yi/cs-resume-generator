"""简历数据模型：整个系统的唯一数据契约。

前端表单、Jinja2 模板渲染、PDF 导出均以此为准；
``schema_version`` 用于后续结构演进时的前向兼容。
"""

from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator

SCHEMA_VERSION = 1

_MONTH_RE = re.compile(r"^(\d{4})-(0[1-9]|1[0-2])$")
_PHONE_RE = re.compile(r"^1[3-9]\d{9}$")
_URL_RE = re.compile(r"^https?://\S+$")

Degree = Literal["专科", "本科", "硕士", "博士"]
Proficiency = Literal["了解", "掌握", "熟练", "精通"]


def _check_month(value: str, label: str, *, allow_now: bool = False) -> str:
    """校验 YYYY-MM 月份格式；结束时间允许「至今」。"""
    value = value.strip()
    if allow_now and value == "至今":
        return value
    if not _MONTH_RE.fullmatch(value):
        hint = "或“至今”" if allow_now else ""
        raise ValueError(f"{label}格式应为 YYYY-MM{hint}，例如 2024-09")
    return value


def _month_key(value: str) -> tuple[int, int]:
    match = _MONTH_RE.fullmatch(value.strip())
    return (int(match.group(1)), int(match.group(2))) if match else (0, 0)


def _check_url(value: str | None, label: str) -> str | None:
    if value is None:
        return None
    value = value.strip()
    if value and not _URL_RE.fullmatch(value):
        raise ValueError(f"{label}应为 http(s):// 开头的合法链接")
    return value or None


class _StrippedModel(BaseModel):
    """去除字符串首尾空格的公共基类。"""

    model_config = ConfigDict(str_strip_whitespace=True)


class Basics(_StrippedModel):
    """基本信息。"""

    name: str = Field(..., min_length=1, max_length=50, description="姓名")
    objective: str = Field(..., min_length=1, max_length=100, description="求职意向岗位")
    phone: str = Field(..., description="11 位大陆手机号")
    email: EmailStr = Field(..., description="邮箱")
    city: str | None = Field(None, max_length=50, description="所在城市")
    github: str | None = Field(None, description="GitHub 主页链接")
    blog: str | None = Field(None, description="个人博客链接")
    photo_url: str | None = Field(None, description="证件照链接（可选）")

    @field_validator("phone")
    @classmethod
    def _validate_phone(cls, value: str) -> str:
        if not _PHONE_RE.fullmatch(value):
            raise ValueError("手机号应为 11 位大陆手机号，如 13800138000")
        return value

    @field_validator("github", "blog", "photo_url")
    @classmethod
    def _validate_urls(cls, value: str | None, info) -> str | None:
        labels = {"github": "GitHub 链接", "blog": "博客链接", "photo_url": "照片链接"}
        return _check_url(value, labels[info.field_name])


class Education(_StrippedModel):
    """教育背景。"""

    school: str = Field(..., min_length=1, max_length=100, description="学校")
    college: str | None = Field(None, max_length=100, description="学院")
    major: str = Field(..., min_length=1, max_length=100, description="专业")
    degree: Degree = Field(..., description="学历")
    start_date: str = Field(..., description="入学年月，YYYY-MM")
    end_date: str = Field(..., description="毕业年月，YYYY-MM 或「至今」")
    gpa_rank: str | None = Field(
        None, max_length=100, description="GPA / 排名，如 GPA 3.8/4.0（前 5%）"
    )
    courses: list[str] = Field(default_factory=list, description="主修课程")

    @field_validator("start_date")
    @classmethod
    def _validate_start(cls, value: str) -> str:
        return _check_month(value, "开始时间")

    @field_validator("end_date")
    @classmethod
    def _validate_end(cls, value: str) -> str:
        return _check_month(value, "结束时间", allow_now=True)

    @model_validator(mode="after")
    def _check_order(self) -> Education:
        if self.end_date != "至今" and _month_key(self.start_date) > _month_key(self.end_date):
            raise ValueError("结束时间不能早于开始时间")
        return self


class SkillItem(_StrippedModel):
    """单条技能。"""

    name: str = Field(..., min_length=1, max_length=50, description="技能名")
    level: Proficiency | None = Field(None, description="熟练度")


class SkillGroup(_StrippedModel):
    """技能分组，如「编程语言」/「框架与中间件」。"""

    category: str = Field(..., min_length=1, max_length=50, description="技能类别")
    items: list[SkillItem] = Field(..., min_length=1, description="技能条目")


class _DatedEntry(_StrippedModel):
    """带起止时间的经历条目基类。"""

    start_date: str = Field(..., description="开始年月，YYYY-MM")
    end_date: str = Field(..., description="结束年月，YYYY-MM 或「至今」")

    @field_validator("start_date")
    @classmethod
    def _validate_start(cls, value: str) -> str:
        return _check_month(value, "开始时间")

    @field_validator("end_date")
    @classmethod
    def _validate_end(cls, value: str) -> str:
        return _check_month(value, "结束时间", allow_now=True)

    @model_validator(mode="after")
    def _check_order(self) -> _DatedEntry:
        if self.end_date != "至今" and _month_key(self.start_date) > _month_key(self.end_date):
            raise ValueError("结束时间不能早于开始时间")
        return self


class ProjectExperience(_DatedEntry):
    """项目经历。"""

    name: str = Field(..., min_length=1, max_length=100, description="项目名称")
    role: str | None = Field(None, max_length=50, description="担任角色")
    tech_stack: list[str] = Field(default_factory=list, description="技术栈")
    highlights: list[str] = Field(..., description="要点描述，建议按 STAR 法则撰写")
    link: str | None = Field(None, description="项目链接")

    @field_validator("link")
    @classmethod
    def _validate_link(cls, value: str | None) -> str | None:
        return _check_url(value, "项目链接")

    @field_validator("highlights")
    @classmethod
    def _validate_highlights(cls, value: list[str]) -> list[str]:
        cleaned = [v.strip() for v in value if v.strip()]
        if not cleaned:
            raise ValueError("项目要点不能为空")
        return cleaned


class InternshipExperience(_DatedEntry):
    """实习经历。"""

    company: str = Field(..., min_length=1, max_length=100, description="公司名称")
    position: str = Field(..., min_length=1, max_length=50, description="实习岗位")
    highlights: list[str] = Field(..., description="工作要点，建议按 STAR 法则撰写")

    @field_validator("highlights")
    @classmethod
    def _validate_highlights(cls, value: list[str]) -> list[str]:
        cleaned = [v.strip() for v in value if v.strip()]
        if not cleaned:
            raise ValueError("实习要点不能为空")
        return cleaned


class CampusExperience(_DatedEntry):
    """校园经历 / 学生工作（可选）。"""

    organization: str = Field(..., min_length=1, max_length=100, description="组织 / 社团")
    role: str | None = Field(None, max_length=50, description="担任职务")
    highlights: list[str] = Field(default_factory=list, description="经历要点")


class Award(_StrippedModel):
    """获奖情况。"""

    name: str = Field(..., min_length=1, max_length=100, description="奖项名称")
    level: str | None = Field(None, max_length=50, description="奖项级别，如国家级 / 省级 / 校级")
    date: str = Field(..., description="获奖时间，YYYY-MM")

    @field_validator("date")
    @classmethod
    def _validate_date(cls, value: str) -> str:
        return _check_month(value, "获奖时间")


class ResumeData(_StrippedModel):
    """简历完整数据。"""

    schema_version: int = SCHEMA_VERSION
    basics: Basics
    education: list[Education] = Field(default_factory=list, description="教育背景")
    skills: list[SkillGroup] = Field(default_factory=list, description="专业技能")
    projects: list[ProjectExperience] = Field(default_factory=list, description="项目经历")
    internships: list[InternshipExperience] = Field(default_factory=list, description="实习经历")
    campus: list[CampusExperience] = Field(default_factory=list, description="校园经历")
    awards: list[Award] = Field(default_factory=list, description="获奖情况")
    self_evaluation: list[str] = Field(default_factory=list, description="自我评价")


class RenderRequest(_StrippedModel):
    """渲染 / 导出请求：简历数据 + 模板选择。"""

    data: ResumeData
    template: str = "classic"
