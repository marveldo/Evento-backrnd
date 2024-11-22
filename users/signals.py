from django.db.models.signals import post_save , post_delete
from .models import Notification , DeviceInfo
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()
def createNotifications(sender,instance : Notification, created : bool, **kwargs ):
    if created : 
        group_name = f'notifications_{instance.user.id}'
        async_to_sync(channel_layer.group_send)(
         group_name,
         {
             'type': 'send_notification',
             'message': f'{instance.message}'
         }
        )

def deleteDevice(sender , instance : DeviceInfo, **kwargs):
    group_name = f'logout_{instance.id}'
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type' : 'send_logout_message',
            'message': 'Device Logged Out'
        }
    )

        
post_save.connect(receiver=createNotifications , sender=Notification )
post_delete.connect(receiver=deleteDevice , sender=DeviceInfo)

