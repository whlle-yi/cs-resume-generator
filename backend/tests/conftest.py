"""pytest 公共夹具。"""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.main import create_app
from app.schemas.resume import ResumeData
from app.services.sample_service import load_sample_resume


@pytest.fixture
def app() -> FastAPI:
    return create_app()


@pytest.fixture
def client(app) -> TestClient:
    return TestClient(app)


@pytest.fixture
def sample_data() -> ResumeData:
    return load_sample_resume()
