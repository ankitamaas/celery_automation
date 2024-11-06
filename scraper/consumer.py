from channels.generic.websocket import AsyncWebsocketConsumer
import json

class FrontendConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        query_string_bytes = self.scope['query_string']
        room_name = f"notification_group"
        self.room_name = room_name
 
        await self.channel_layer.group_add(room_name, self.channel_name)
        await self.accept()
        print(f"User {room_name} connected from WebSocket")


    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        print(f"User {self.room_name} disconnected from WebSocket")


    async def receive(self,text_data):
        chat_notification_obj = json.loads(text_data)


    # Hander part
    async def chat_notification(self, event):
        print("Notifications Event...", event)

        type = event['type']
        keyword = event['keyword']
        scheduled_time = event['scheduled_time']
        await self.send(json.dumps({
            'type': type,
            'keyword': keyword,
            'scheduled_time': scheduled_time,
        }))