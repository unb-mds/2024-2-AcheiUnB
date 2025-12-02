from rest_framework import serializers

from users.models import Item

from .models import ChatRoom, Message
from .utils import count_graphemes


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.SerializerMethodField()

    def get_sender_username(self, obj):
        return obj.sender.first_name or obj.sender.last_name or obj.sender.username

    def validate_content(self, value):

        grapheme_count = count_graphemes(value)
        if grapheme_count > 80:
            raise serializers.ValidationError(
                f"A mensagem não pode ter mais de 80 caracteres. "
                f"Você usou {grapheme_count} caracteres."
            )
        return value

    class Meta:
        model = Message
        fields = ["id", "room", "sender", "sender_username", "content", "timestamp", "is_read"]
        read_only_fields = ["sender"]


class ChatRoomSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    participant_1_username = serializers.SerializerMethodField()
    participant_2_username = serializers.SerializerMethodField()
    item_id = serializers.IntegerField(required=True)
    item_name = serializers.ReadOnlyField(source="item.name")
    unread_count = serializers.SerializerMethodField()

    def get_unread_count(self, obj):
        """Retorna a quantidade de mensagens não lidas pelo usuário da requisição"""
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return 0

        # Obter o usuário atual
        current_user = request.user

        # Contar mensagens não lidas (enviadas por outros usuários)
        return (
            Message.objects.filter(room=obj, is_read=False)
            .exclude(sender=current_user)
            .count()
        )

    def get_participant_1_username(self, obj):
        return (
            obj.participant_1.first_name
            or obj.participant_1.last_name
            or obj.participant_1.username
        )

    def get_participant_2_username(self, obj):
        return (
            obj.participant_2.first_name
            or obj.participant_2.last_name
            or obj.participant_2.username
        )

    class Meta:
        model = ChatRoom
        fields = [
            "id",
            "participant_1",
            "participant_1_username",
            "participant_2",
            "participant_2_username",
            "item_id",
            "item_name",
            "unread_count",
            "created_at",
            "messages",
        ]

    def validate_item_id(self, value):
        if not Item.objects.filter(id=value).exists():
            raise serializers.ValidationError("O item associado não foi encontrado.")
        return value

    def create(self, validated_data):
        item_id = validated_data.pop("item_id")
        validated_data["item"] = Item.objects.get(id=item_id)

        chat_room = super().create(validated_data)
        return chat_room
