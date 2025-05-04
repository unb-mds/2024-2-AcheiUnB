from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from chat.models import ChatRoom, Message
from users.models import Item


class ChatRoomViewSetTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")
        self.item = Item.objects.create(name="Celular Perdido", status="lost")

        self.client.force_authenticate(user=self.user1)

    def test_create_chat_room_success(self):
        data = {
            "participant_1": self.user1.id,
            "participant_2": self.user2.id,
            "item_id": self.item.id,
        }
        response = self.client.post("/api/chat/chatrooms/", data)

        assert response.status_code == status.HTTP_201_CREATED
        assert ChatRoom.objects.count() == 1

    def test_create_chat_room_duplicate(self):
        ChatRoom.objects.create(
            participant_1=self.user1, participant_2=self.user2, item=self.item
        )

        data = {
            "participant_2": self.user2.id,
            "item_id": self.item.id,
        }
        response = self.client.post("/api/chat/chatrooms/", data)

        assert response.status_code == status.HTTP_200_OK
        # O que o código realmente retorna é o chat existente
        assert response.data["participant_1"] == self.user1.id
        assert response.data["participant_2"] == self.user2.id
        assert response.data["item_id"] == self.item.id

    def test_create_chat_missing_fields(self):
        # participant_2 e item_id faltando
        data = {}
        response = self.client.post("/api/chat/chatrooms/", data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Os campos participant_2 e item são obrigatórios." in str(response.data)

    def test_create_chat_with_self(self):
        data = {
            "participant_1": self.user1.id,
            "participant_2": self.user1.id,
            "item_id": self.item.id,
        }
        response = self.client.post("/api/chat/chatrooms/", data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Não é possível criar um chat consigo mesmo." in str(response.data)

    def test_create_chat_with_invalid_item(self):
        data = {
            "participant_1": self.user1.id,
            "participant_2": self.user2.id,
            "item_id": 9999,  # ID de item que não existe
        }
        response = self.client.post("/api/chat/chatrooms/", data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "O item associado não foi encontrado." in str(response.data)


class MessageViewSetTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")
        self.item = Item.objects.create(name="Chave Achada", status="found")
        self.chat_room = ChatRoom.objects.create(
            participant_1=self.user1, participant_2=self.user2, item=self.item
        )

        self.client.force_authenticate(user=self.user1)

        Message.objects.all().delete()

    def test_send_message_success(self):
        data = {
            "room": self.chat_room.id,
            "content": "Olá, achei seu item!",
        }
        response = self.client.post("/api/chat/messages/", data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Message.objects.count() == 1
        assert Message.objects.first().sender == self.user1

    def test_get_messages_from_chat_room(self):
        Message.objects.create(room=self.chat_room, sender=self.user1, content="Oi!")
        Message.objects.create(room=self.chat_room, sender=self.user2, content="Olá!")

        response = self.client.get(f"/api/chat/messages/?room={self.chat_room.id}")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2

    def test_send_empty_message_fails(self):
        data = {
            "room": self.chat_room.id,
            "content": "",  # Conteúdo vazio
        }
        response = self.client.post("/api/chat/messages/", data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "content" in response.data

    def test_send_message_unauthenticated_fails(self):
        self.client.logout()
        data = {
            "room": self.chat_room.id,
            "content": "Mensagem sem estar logado",
        }
        response = self.client.post("/api/chat/messages/", data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_messages_pagination(self):
        for i in range(15):
            Message.objects.create(
                room=self.chat_room, sender=self.user1, content=f"Mensagem {i}"
            )

        response = self.client.get(f"/api/chat/messages/?room={self.chat_room.id}")

        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data
        assert len(response.data["results"]) == 15

    def test_get_queryset_filters_by_room(self):
        other_item = Item.objects.create(name="Carteira", status="found")
        other_chat = ChatRoom.objects.create(
            participant_1=self.user1, participant_2=self.user2, item=other_item
        )

        msg1 = Message.objects.create(
            room=self.chat_room, sender=self.user1, content="Mensagem na sala 1"
        )
        msg2 = Message.objects.create(
            room=other_chat, sender=self.user2, content="Mensagem na sala 2"
        )

        response = self.client.get(f"/api/chat/messages/?room={self.chat_room.id}")

        assert response.status_code == status.HTTP_200_OK
        returned_ids = [msg["id"] for msg in response.data["results"]]
        assert msg1.id in returned_ids
        assert msg2.id not in returned_ids


class ClearChatsViewTests(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(username="admin", password="password")
        self.user = User.objects.create_user(username="user", password="password")

        self.client.force_authenticate(user=self.admin_user)

        self.item = Item.objects.create(name="Carteira Perdida", status="lost")
        self.chat_room = ChatRoom.objects.create(
            participant_1=self.user, participant_2=self.admin_user, item=self.item
        )
        self.message = Message.objects.create(
            room=self.chat_room, sender=self.user, content="Alguém achou?"
        )

    def test_clear_chats_admin_success(self):
        response = self.client.delete("/api/chat/clear_chats/")

        assert response.status_code == status.HTTP_200_OK
        assert ChatRoom.objects.count() == 0
        assert Message.objects.count() == 0

    def test_clear_chats_non_admin_forbidden(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete("/api/chat/clear_chats/")

        assert response.status_code == status.HTTP_403_FORBIDDEN
