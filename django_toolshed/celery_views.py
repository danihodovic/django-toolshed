import logging

from celery import current_app
from celery.result import AsyncResult
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet


# pylint: disable=abstract-method
class TaskSerializer(serializers.Serializer):
    task_name = serializers.CharField()
    args = serializers.ListField(required=False)
    kwargs = serializers.DictField(required=False)


# pylint: disable=no-self-use
class CeleryTaskViewSet(ViewSet):
    def retrieve(self, request, pk=None):
        result = AsyncResult(pk)
        return Response(dict(task_id=result.task_id, status=result.status))

    def create(self, request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task_name = serializer.data["task_name"]
        worker_tasks = registered_tasks()
        task_arguments = serializer.data
        task_arguments.pop("task_name")
        if task_name not in worker_tasks:
            raise NotFound(f"{task_name=} not found in registered {worker_tasks=}")
        sent_task = current_app.send_task(task_name, **task_arguments)
        logging.info(f"Triggered celery {task_name=} with {task_arguments=}")
        return Response(
            data={**serializer.data, "task_id": sent_task.task_id}, status=201
        )


class TaskTypesView(APIView):
    # pylint: disable=redefined-builtin,unused-argument
    def get(self, request, format=None):
        worker_tasks = registered_tasks()
        # Return trigger url
        return Response({"task_types": worker_tasks})


def registered_tasks():
    registered = current_app.control.inspect().registered()
    if not registered:
        raise ParseError(
            (
                "No registered tasks. Are you sure your app is "
                "configured and at least one worker is running?"
            ),
        )
    worker_tasks = [item for sublist in registered.values() for item in sublist]
    return worker_tasks
