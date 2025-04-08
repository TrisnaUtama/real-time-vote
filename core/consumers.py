import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PollConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "all_polls",
            self.channel_name
        )
        
        poll_id = self.scope['url_route']['kwargs'].get('poll_id')
        if poll_id:
            await self.channel_layer.group_add(
                f"poll_{poll_id}",
                self.channel_name
            )
        
        await self.accept()
        print(f"✅ WebSocket Connected to groups: all_polls and poll_{poll_id if poll_id else ''}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "all_polls",
            self.channel_name
        )
        
        poll_id = self.scope['url_route']['kwargs'].get('poll_id')
        if poll_id:
            await self.channel_layer.group_discard(
                f"poll_{poll_id}",
                self.channel_name
            )

    async def poll_update(self, event):
        await self.send(text_data=json.dumps(event['data']))