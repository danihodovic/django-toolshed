from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "List installed django apps"

    def handle(self, *args, **options):
        for app in apps.get_app_configs():
            print(app.label)
