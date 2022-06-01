import os

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture(scope="session")
def celery_config():
    broker_host = "localhost"
    if os.path.isfile("/.dockerenv"):
        broker_host = "redis"
    return {"broker_url": f"redis://{broker_host}:6379"}
