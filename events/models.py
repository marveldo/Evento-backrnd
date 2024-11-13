from django.db import models
from users.models import User
import uuid
from django.utils import timezone


# Create your models here.

class EventTag(models.Model):
     id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
     tag_name = models.CharField(max_length=550, blank=True, null=True)

     def __str__(self) -> str:
         return str(self.tag_name)
     
class Event(models.Model):
    event_name = models.CharField(max_length=250, blank=True , null=True)
    date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_date =  models.DateField(blank=True, null=True)
    start_time = time =models.TimeField(blank =True, null=True)
    time =models.TimeField(blank =True, null=True)
    price = models.IntegerField(default= 0, blank=True , null=True)
    location = models.CharField(max_length=400, blank=True , null=True)
    event_image = models.ImageField(blank=True, null=True, upload_to='images/events')
    capacity = models.IntegerField(blank=True, null=True, default=0)
    created_by = models.CharField(blank=True, null=True, max_length=650)
    users = models.ManyToManyField(User)
    tags = models.ManyToManyField(EventTag)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True )

    def __str__(self) -> str:
        return str(self.event_name)
    
    class Meta :
        ordering = ['-created_at']
    

