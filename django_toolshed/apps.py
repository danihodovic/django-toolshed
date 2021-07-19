from django.apps import AppConfig


class DjangoToolsConfig(AppConfig):
    name = "django_toolshed"

    def ready(self):
        try:
            # pylint: disable=unused-import,import-outside-toplevel
            import django_toolshed.signals
        except ImportError:
            pass
