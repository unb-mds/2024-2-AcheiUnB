from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from chat.models import ChatRoom, Message
from chat.serializers import ChatRoomSerializer, MessageSerializer
from users.models import Item

User = get_user_model()


class ChatRoomSerializerTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1",
            email="user1@example.com",
            password="password1",
            first_name="User1",
        )
        self.user2 = User.objects.create_user(
            username="user2",
            email="user2@example.com",
            password="password2",
            first_name="User2",
        )

        self.item = Item.objects.create(name="Carteira Perdida", user=self.user1)

        self.chat_room = ChatRoom.objects.create(
            participant_1=self.user1,
            participant_2=self.user2,
            item=self.item,
        )

    def test_chat_room_serializer_valid_data(self):
        serializer = ChatRoomSerializer(instance=self.chat_room)
        data = serializer.data

        assert data["participant_1"] == self.user1.id
        assert data["participant_2"] == self.user2.id
        assert data["participant_1_username"] == self.user1.first_name
        assert data["participant_2_username"] == self.user2.first_name
        assert data["item_id"] == self.item.id
        assert data["item_name"] == self.item.name
        assert data["messages"] == []

    def test_chat_room_serializer_create(self):
        data = {
            "participant_1": self.user1.id,
            "participant_2": self.user2.id,
            "item_id": self.item.id,
        }
        serializer = ChatRoomSerializer(data=data)

        assert serializer.is_valid(), serializer.errors
        chat_room = serializer.save()

        assert chat_room.participant_1 == self.user1
        assert chat_room.participant_2 == self.user2
        assert chat_room.item == self.item

    def test_chat_room_serializer_invalid_item(self):
        data = {
            "participant_1": self.user1.id,
            "participant_2": self.user2.id,
            "item_id": 99999,
        }
        serializer = ChatRoomSerializer(data=data)

        assert not serializer.is_valid()
        assert "item_id" in serializer.errors
        assert serializer.errors["item_id"][0] == "O item associado não foi encontrado."


class MessageSerializerTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1",
            email="user1@example.com",
            password="password1",
            first_name="User1",
        )
        self.user2 = User.objects.create_user(
            username="user2",
            email="user2@example.com",
            password="password2",
            first_name="User2",
        )

        self.item = Item.objects.create(name="Chave Perdida", user=self.user1)
        self.chat_room = ChatRoom.objects.create(
            participant_1=self.user1,
            participant_2=self.user2,
            item=self.item,
        )

        self.message = Message.objects.create(
            room=self.chat_room, sender=self.user1, content="Oi, achei sua carteira!"
        )

    def test_message_serializer_valid_data(self):
        serializer = MessageSerializer(instance=self.message)
        data = serializer.data

        assert data["room"] == self.chat_room.id
        assert data["sender"] == self.user1.id
        assert data["sender_username"] == self.user1.first_name
        assert data["content"] == "Oi, achei sua carteira!"
