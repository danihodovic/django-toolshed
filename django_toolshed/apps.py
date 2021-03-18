from django.apps import AppConfig


class DjangoToolsConfig(AppConfig):
    name = "django_toolshed"

    def ready(self):
        try:
            # pylint: disable=unused-import
            import django_toolshed.signals
        except ImportError:
            pass
