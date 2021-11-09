from django.contrib import admin

from django_toolshed.mixins import LinkRelatedMixin

from .models import Property


@admin.register(Property)
class PropertyAdmin(LinkRelatedMixin, admin.ModelAdmin):
    list_display = ["owner__link"]
