from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from chat.models import ChatRoom, Message
from users.models import Item

"""class ChatRoomViewSetTests(APITestCase):

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
            "participant_1": self.user1.id,
            "participant_2": self.user2.id,
            "item_id": self.item.id,
        }
        response = self.client.post("/api/chat/chatrooms/", data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Já existe um chat para este item com os mesmos participantes."
        in response.data"""


class ChatRoomViewSetTests(APITestCase):
    def setUp(self):
        # Criando usuários
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="password1"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="password2"
        )

        # Criando um item de teste
        self.item = Item.objects.create(name="Carteira Perdida", user=self.user1)

        # Definindo a URL da API
        self.url = "/api/chat/chatrooms/"

        # Autenticando o primeiro usuário
        self.client.force_authenticate(user=self.user1)

    # def test_create_chatroom_success(self):
    #     """Teste para criação bem-sucedida de uma sala de chat entre dois usuários"""
    #     data = {"participant_2": self.user2.id, "item_id": self.item.id}
    #     response = self.client.post(self.url, data, format="json")

    #     print("Response Data:", response.data)  # <--- Adicionado para depuração
    #     assert response.status_code == status.HTTP_201_CREATED

    def test_create_chatroom_missing_fields(self):
        """Teste para erro ao tentar criar uma sala de chat sem os campos obrigatórios"""
        response = self.client.post(self.url, {}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Os campos participant_2 e item são obrigatórios." in str(response.data)

    def test_create_chatroom_with_self(self):
        """Teste para erro ao tentar criar uma sala de chat consigo mesmo"""
        data = {"participant_2": self.user1.id, "item_id": self.item.id}
        response = self.client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Não é possível criar um chat consigo mesmo." in str(response.data)

    def test_create_chatroom_with_nonexistent_item(self):
        """Teste para erro ao tentar criar uma sala de chat com um item inexistente"""
        data = {"participant_2": self.user2.id, "item_id": 99999}  # ID de item que não existe
        response = self.client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "O item associado não foi encontrado." in str(response.data)

    def test_create_chatroom_when_already_exists(self):
        """Teste para retornar a sala de chat existente se já houver uma criada"""
        # Criando a sala de chat inicialmente
        chatroom = ChatRoom.objects.create(
            participant_1=self.user1, participant_2=self.user2, item=self.item
        )

        data = {"participant_2": self.user2.id, "item_id": self.item.id}
        response = self.client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert ChatRoom.objects.count() == 1  # Apenas uma sala deve existir
        assert response.data["id"] == chatroom.id  # Deve retornar o chatroom existente


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
