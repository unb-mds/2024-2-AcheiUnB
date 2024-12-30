from django.db import models
from django.contrib.auth.models import User


class ChatRoom(models.Model):
    """Representa uma sala de chat entre dois usuários."""
    participant_1 = models.ForeignKey(User, related_name="chatrooms_as_participant_1", on_delete=models.CASCADE)
    participant_2 = models.ForeignKey(User, related_name="chatrooms_as_participant_2", on_delete=models.CASCADE)
    item_description = models.CharField(max_length=250, blank=True, null=True)  # Descrição do item perdido (opcional)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between {self.participant_1.username} and {self.participant_2.username}"


class Message(models.Model):
    """Armazena mensagens em um chat."""
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages", null=True, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"
