from channels.generic.websocket import AsyncWebsocketConsumer
import json
import logging
class BaseWebsocketConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        user = self.scope['user']
        if user.is_anonymous:
            logging.info("Not authenticated")
            await self.close(code=4401, reason='Unauthenticated')
        else :
            await self.accept()
            await self.send(json.dumps({
           'message': f'Hello welcome to the websocket {user.email}',
           'detail': 'Connection Successful'
            }))
    