from django.urls import path
from rest_framework import routers

from django_toolshed.celery_views import CeleryTaskViewSet, TaskTypesView

app_name = "django_toolshed:celery"


router = routers.SimpleRouter()
router.register(r"tasks", CeleryTaskViewSet, basename="task")
urlpatterns = router.urls + [
    path("task-types/", TaskTypesView.as_view(), name="task-types"),
]
