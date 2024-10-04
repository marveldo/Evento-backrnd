from django.db import models
from users.models import User
import uuid
# Create your models here.

class EventTag(models.Model):
     tag_name = models.CharField(max_length=550, blank=True, null=True)

     def __str__(self) -> str:
         return str(self.tag_name)
     
class Event(models.Model):
    event_name = models.CharField(max_length=250, blank=True , null=True)
    date = models.DateField(blank=True, null=True)
    start_date =  models.DateField(blank=True, null=True)
    start_time = time =models.TimeField(blank =True, null=True)
    time =models.TimeField(blank =True, null=True)
    price = models.IntegerField(default= 0, blank=True , null=True)
    location = models.CharField(max_length=400, blank=True , null=True)
    event_image = models.ImageField(blank=True, null=True, upload_to='images/events')
    capacity = models.IntegerField(blank=True, null=True, default=0)
    users = models.ManyToManyField(User)
    tags = models.ManyToManyField(EventTag)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True )

    def __str__(self) -> str:
        return str(self.event_name)

