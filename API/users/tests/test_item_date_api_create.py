import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_api_create_rejects_too_old_date():

    client = APIClient()

    user = User.objects.create_user(
        username="api_tester",
        email="api@test.com",
        password="123"
    )
    client.force_authenticate(user=user)

    data = {
        "name": "Item API Antigo",
        "status": "lost",
        "found_lost_date": "1830-04-19T00:00:00Z",
        "category": 1,
        "location": 1
    }

    url = reverse("item-list")

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "found_lost_date" in response.json()
