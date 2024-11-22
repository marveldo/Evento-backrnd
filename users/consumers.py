from channels.generic.websocket import AsyncWebsocketConsumer
import json
import logging

class NotificationsConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']
        self.group_name='disconnect'
        self.second_group_name = 'logout'
        if user.is_anonymous:
            logging.info('Not Authenticated')
            await self.close(code=4401, reason='Authentication error')
        else :
            self.group_name=f'notifications_{user.id}'
            device_id = self.scope['device_id']
            self.second_group_name = f'logout_{device_id}'
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.channel_layer.group_add(
                self.second_group_name,
                self.channel_name
            )
            await self.accept()
    
    async def send_notification(self, event):
        message = event['message']
        await self.send(json.dumps({
            'detail': 'Notification Message',
            'message': message
        }))
    
    async def send_logout_message(self , event):
        await self.close(code=4401 , reason='This device has been logged Out')

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        await self.channel_layer.group_discard(
            self.second_group_name,
            self.channel_name
        )

