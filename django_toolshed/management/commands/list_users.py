from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.apps import apps

User = get_user_model()


class Command(BaseCommand):
    help = "List installed django apps"

    def handle(self, *args, **options):
        for user in User.objects.all():
            print(user.username)
