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
