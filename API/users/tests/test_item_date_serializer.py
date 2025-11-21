import pytest
from users.serializers import ItemSerializer

@pytest.mark.django_db
def test_serializer_rejects_old_date():
    data = {
        "name": "Carteira",
        "status": "lost",
        "found_lost_date": "1830-04-19T00:00:00Z",
    }
    s = ItemSerializer(data=data)
    assert not s.is_valid()
    assert "found_lost_date" in s.errors


@pytest.mark.django_db
def test_serializer_accepts_valid_date():
    data = {
        "name": "Chave",
        "status": "lost",
        "found_lost_date": "2023-01-01T00:00:00Z",
    }
    s = ItemSerializer(data=data)
    assert s.is_valid(), s.errors