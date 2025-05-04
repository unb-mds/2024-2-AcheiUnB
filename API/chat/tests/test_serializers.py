import pytest
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from chat.serializers import ChatRoomSerializer
from users.models import Item


class ChatRoomSerializerTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user", password="password")
        self.valid_item = Item.objects.create(name="Mochila", status="lost")

    def test_validate_item_id_success(self):
        serializer = ChatRoomSerializer()
        validated_value = serializer.validate_item_id(self.valid_item.id)
        assert validated_value == self.valid_item.id

    def test_validate_item_id_invalid(self):
        serializer = ChatRoomSerializer()
        invalid_id = 9999  # ID que não existe

        with pytest.raises(ValidationError) as exc_info:
            serializer.validate_item_id(invalid_id)

        assert "O item associado não foi encontrado." in str(exc_info.value)
