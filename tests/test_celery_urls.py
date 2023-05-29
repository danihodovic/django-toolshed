import time

import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


# A worker needs to run for Celery to find registered tasks
# pylint: disable=unused-argument
def test_triggers_task(api_client, celery_worker):
    url = reverse("celery:task-list")
    res = api_client.post(url, dict(task_name="tests.celery_app.debug_task"))
    assert res.status_code == 201, res.data
    assert res.data == {
        "task_id": res.data["task_id"],
        "status": "pending",
    }


def test_triggers_nonexisting_task(api_client, celery_worker):
    url = reverse("celery:task-list")
    res = api_client.post(url, dict(task_name="noop"))
    assert res.status_code == 404
    assert res.json() == {
        "detail": "task_name='noop' not found in registered worker_tasks=['tests.celery_app.debug_task']"
    }


def test_retrieves_task(api_client, celery_worker):
    url = reverse("celery:task-list")
    res = api_client.post(url, dict(task_name="tests.celery_app.debug_task"))
    assert res.status_code == 201, res.data
    url = reverse("celery:task-detail", args=[res.data["task_id"]])
    res = api_client.get(url)
    assert {
        "task_id": res.data["task_id"],
        "status": "pending",
    } == res.data
    time.sleep(1)
    res = api_client.get(url)
    assert res.data["status"] == "success"


def test_retrieve_nonexisting_task(api_client, celery_worker):
    url = reverse("celery:task-detail", args=["b4f284de-6695-4dfa-9083-36b937cbd0ef"])
    res = api_client.get(url)
    assert res.data == {
        "task_id": "b4f284de-6695-4dfa-9083-36b937cbd0ef",
        "status": "pending",
    }


def test_task_types_view(api_client, celery_worker):
    url = reverse("celery:task-types")
    res = api_client.get(url)
    assert res.status_code == 200
    assert res.data == {"task_types": ["tests.celery_app.debug_task"]}
