from rest_framework import routers

from django_toolshed.celery_views import CeleryTaskViewSet

app_name = "django_toolshed:celery"


router = routers.SimpleRouter()
router.register(r"tasks", CeleryTaskViewSet, basename="task")
urlpatterns = router.urls
