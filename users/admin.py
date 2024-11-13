from django.contrib import admin
from .models import User,Notification,DeviceInfo
# Register your models here.


admin.site.register(User)
admin.site.register(Notification)
admin.site.register(DeviceInfo)