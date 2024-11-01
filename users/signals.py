from django.db.models.signals import post_save
from .models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()
def createNotifications(sender,instance, created : bool, **kwargs ):
    if created : 
        group_name = f'notifications_{instance.user.id}'
        async_to_sync(channel_layer.group_send)(
         group_name,
         {
             'type': 'send_notification',
             'message': f'{instance.message}'
         }
        )
        
post_save.connect(receiver=createNotifications , sender=Notification )

