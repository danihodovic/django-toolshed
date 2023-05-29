# pylint: disable=abstract-method
import logging

from celery import current_app
from celery.result import AsyncResult
from celery.states import ALL_STATES
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class CreateTaskSerializer(serializers.Serializer):
    task_name = serializers.CharField()
    args = serializers.ListField(required=False)
    kwargs = serializers.DictField(required=False)


class ReadTaskSerializer(serializers.Serializer):
    task_id = serializers.CharField()
    status = serializers.ChoiceField(
        choices=[(v.lower(), v.capitalize()) for v in sorted(ALL_STATES)]
    )


class CeleryTaskViewSet(ViewSet):
    serializer_class = None

    @extend_schema(
        operation_id="read_task_status",
        parameters=[
            OpenApiParameter(
                name="id", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH
            )
        ],
        responses={200: ReadTaskSerializer},
    )
    def retrieve(self, request, pk=None, **kwargs):
        async_result = AsyncResult(pk)
        serializer = ReadTaskSerializer(
            data=dict(
                task_id=async_result.task_id,
                status=async_result.status.lower(),
            )
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    @extend_schema(
        operation_id="create_task",
        request=CreateTaskSerializer,
        responses={201: ReadTaskSerializer},
    )
    def create(self, request):
        serializer = CreateTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task_name = serializer.data["task_name"]

        worker_tasks = registered_tasks()
        if task_name not in worker_tasks:
            raise NotFound(f"{task_name=} not found in registered {worker_tasks=}")

        async_result = current_app.send_task(
            name=task_name,
            args=serializer.data.get("args"),
            kwargs=serializer.data.get("kwargs"),
        )
        logging.info(f"Triggered celery {task_name=} via HTTP request")
        serializer = ReadTaskSerializer(
            data=dict(
                task_id=async_result.task_id,
                status=async_result.status.lower(),
            )
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=201)

    @action(detail=False, methods=["GET"])
    def types(self, request):
        worker_tasks = registered_tasks()
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
