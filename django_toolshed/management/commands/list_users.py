from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "List installed django apps"

    def handle(self, *args, **options):
        for user in User.objects.all():
            print(user.username)
