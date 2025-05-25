from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from chat.models import ChatRoom, Message
from users.models import Item
from users.pagination import ChatPagination
from users.tasks import delete_old_messages

from .serializers import ChatRoomSerializer, MessageSerializer


class ChatRoomViewSet(ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Cria uma nova sala de chat entre dois usuários "
        + "para um item específico.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "participant_2": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="ID do segundo participante."
                ),
                "item_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="ID do item associado à conversa."
                ),
            },
            required=["participant_2", "item_id"],
        ),
        responses={
            201: openapi.Response("Sala de chat criada", ChatRoomSerializer),
            400: "Erro de validação",
        },
    )
    def create(self, request, *args, **kwargs):
        participant_1_id = request.user.id
        participant_2_id = request.data.get("participant_2")
        item_id = request.data.get("item_id")

        if not participant_2_id or not item_id:
            raise ValidationError("Os campos participant_2 e item são obrigatórios.")

        if participant_1_id == int(participant_2_id):
            raise ValidationError("Não é possível criar um chat consigo mesmo.")

        if not Item.objects.filter(id=item_id).exists():
            raise ValidationError("O item associado não foi encontrado.")

        existing_chat = ChatRoom.objects.filter(
            participant_1=participant_1_id, participant_2=participant_2_id, item_id=item_id
        ).first()

        if existing_chat:
            return Response(self.get_serializer(existing_chat).data)

        return super().create(request, *args, **kwargs)


class MessageViewSet(ModelViewSet):
    """ViewSet para gerenciar mensagens."""

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ChatPagination

    @swagger_auto_schema(
        operation_description="Lista todas as mensagens de uma sala de chat específica.",
        manual_parameters=[
            openapi.Parameter(
                "room",
                openapi.IN_QUERY,
                description="ID da sala de chat",
                type=openapi.TYPE_INTEGER,
            )
        ],
        responses={200: openapi.Response("Lista de mensagens", MessageSerializer(many=True))},
    )
    def get_queryset(self):
        room_id = self.request.query_params.get("room")
        if room_id:
            return Message.objects.filter(room_id=room_id).order_by("timestamp")
        return super().get_queryset().order_by("timestamp")

    @swagger_auto_schema(
        operation_description="Envia uma nova mensagem em uma sala de chat.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "room": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="ID da sala de chat"
                ),
                "content": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Conteúdo da mensagem"
                ),
            },
            required=["room", "content"],
        ),
        responses={201: openapi.Response("Mensagem enviada", MessageSerializer)},
    )
    def perform_create(self, serializer):
        message = serializer.save(sender=self.request.user)
        delete_old_messages.delay(message.room_id)


class ClearChatsView(APIView):
    """Endpoint para limpar todas as mensagens e/ou salas de chat."""

    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="Deleta todas as mensagens e salas de chat do sistema.",
        responses={200: "Todos os chats foram limpos com sucesso."},
    )
    def delete(self, request, *args, **kwargs):
        Message.objects.all().delete()
        ChatRoom.objects.all().delete()
        return Response({"detail": "Todos os chats foram limpos com sucesso."})
