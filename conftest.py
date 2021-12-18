import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture(scope="session")
def celery_config():
    return {"broker_url": "redis://localhost:6379"}
