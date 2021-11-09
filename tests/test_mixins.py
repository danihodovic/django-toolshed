from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Property

User = get_user_model()


def test_renders_admin_link(admin_client):
    user = User.objects.first()
    Property.objects.create(owner=user)
    res = admin_client.get(reverse("admin:tests_property_changelist"))
    soup = BeautifulSoup(res.content)
    link = soup.select_one(".related-link")
    assert link.attrs["href"] == reverse("admin:auth_user_change", args=[user.id])
