from channels.generic.websocket import AsyncWebsocketConsumer
import json
import logging

class NotificationsConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']
        self.group_name='disconnect'
        if user.is_anonymous:
            logging.info('Not Authenticated')
            await self.close(code=4401, reason='Authentication error')
        else :
            self.group_name=f'notifications_{user.id}'
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
    
    async def send_notification(self, event):
        message = event['message']
        await self.send(json.dumps({
            'detail': 'Notification Message',
            'message': message
        }))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

