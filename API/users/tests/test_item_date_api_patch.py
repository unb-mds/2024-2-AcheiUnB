import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User

@pytest.mark.django_db
def test_api_patch_rejects_too_old_date():
    
    client = APIClient()
    
    user = User.objects.create_user(username="patch_tester", email="patch@test.com", password="123")
    client.force_authenticate(user=user)

    url_create = reverse("item-list")
    data_valid = {
        "name": "Item Valido",
        "status": "lost",
        "found_lost_date": "2024-01-01T12:00:00Z",
        "category_id": 1, 
        "location_id": 1
    }
    response_create = client.post(url_create, data_valid, format='json')
    assert response_create.status_code == status.HTTP_201_CREATED
    item_id = response_create.json()['id']

    url_patch = reverse("item-detail", args=[item_id])
    data_invalid = {
        "found_lost_date": "1830-04-19T00:00:00Z"
    }
    
    response_patch = client.patch(url_patch, data_invalid, format='json')

    assert response_patch.status_code == status.HTTP_400_BAD_REQUEST
    assert "found_lost_date" in response_patch.json()