import json
from channels.generic.websocket import AsyncWebsocketConsumer


class QueueConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.queue_id = self.scope["url_route"]["kwargs"]["queue_id"]
        self.room_group_name = f"queue_{self.queue_id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get("type") == "queue_update":
            # Broadcast to group
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "queue_update", "data": data["data"]},
            )

    async def queue_update(self, event):
        await self.send(
            text_data=json.dumps({"type": "queue_update", "data": event["data"]})
        )
