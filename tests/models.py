from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Property(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
