from django.contrib.auth.models import User
from django.db import models

from users.models import Item


class ChatRoom(models.Model):
    """Representa uma sala de chat entre dois usuários."""

    participant_1 = models.ForeignKey(
        User, related_name="chatrooms_as_participant_1", on_delete=models.CASCADE
    )
    participant_2 = models.ForeignKey(
        User, related_name="chatrooms_as_participant_2", on_delete=models.CASCADE
    )
    item = models.ForeignKey(
        Item, related_name="chatrooms", on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between {self.participant_1.username} and {self.participant_2.username}"


class Message(models.Model):
    """Armazena mensagens em um chat."""

    room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name="messages",
        null=True,
        blank=True,
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    notification_sent = models.BooleanField(default=False)

    def clean(self):
        from django.core.exceptions import ValidationError

        from .utils import count_graphemes

        super().clean()

        if not self.content or not self.content.strip():
            raise ValidationError({"content": "A mensagem não pode ser vazia."})

        grapheme_count = count_graphemes(self.content)
        if grapheme_count > 80:
            raise ValidationError(
                {
                    "content": f"A mensagem não pode ter mais de 80 caracteres. "
                    f"Você usou {grapheme_count} caracteres."
                }
            )

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"
