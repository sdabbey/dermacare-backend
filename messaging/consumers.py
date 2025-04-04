import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group_name = f"chat_{self.chat_id}"

        # Add the user to the group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Remove the user from the group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get("message")  # Ensure key exists
            sender = data.get("sender", "Unknown")
            chat_id = data.get("chat_id")

            if not message or not chat_id:
                return  # Don't process empty messages or missing chat_id

            # Broadcast the message to the chat group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "sender": sender,
                },
            )
        except json.JSONDecodeError:
            print("Invalid WebSocket message format")

    async def chat_message(self, event):
        """ Send message to WebSocket """
        await self.send(text_data=json.dumps(event))
