# mypy: ignore-errors
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html


class UserURLMixin:  # pylint: disable=too-few-public-methods,no-self-use
    def user_url(self, obj):
        if not obj.user:
            return "-"
        url = reverse("admin:users_user_change", args=[obj.user.id])
        return format_html(
            '<a href="{}">{}</a>', url, obj.user.email or obj.user.username
        )

    user_url.short_description = "User"  # type: ignore


# pylint: disable=too-few-public-methods
class LinkRelatedMixin:
    def __init__(self, *args, **kwargs):
        self.original_list_display = self.list_display
        self.list_display = [
            entry for entry in self.list_display if not entry.endswith("__link")
        ]
        super().__init__(*args, **kwargs)
        for entry in self.original_list_display:
            if entry.endswith("__link"):
                self.add_foreign_key_link(entry)
        self.list_display = self.original_list_display

    def add_foreign_key_link(self, link_name):
        field_name = link_name.replace("__link", "")
        model_field = getattr(self.model, field_name).field
        related_fields = model_field.resolve_related_fields()
        related_model = related_fields[0][0].related_model
        app = related_model._meta.app_label
        name = related_model._meta.verbose_name

        @admin.display(description=field_name.capitalize())
        def fn(obj):
            related_instance = getattr(obj, field_name)
            url = reverse(f"admin:{app}_{name}_change", args=[related_instance.id])
            return format_html(
                '<a class="related-link" href="{}">{}</a>', url, related_instance
            )

        setattr(self, f"{link_name}", fn)
