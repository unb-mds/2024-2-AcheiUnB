import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.chat_group_name = f"chat_{self.chat_id}"

        # Join the chat group
        await self.channel_layer.group_add(self.chat_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the chat group
        await self.channel_layer.group_discard(self.chat_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]

        # Send message to the group
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                "type": "chat_message",
                "message": message,
            },
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                }
            )
        )