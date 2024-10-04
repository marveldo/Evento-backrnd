from rest_framework import serializers
from .models import Event



class EventSerializer(serializers.ModelSerializer):
    event_category = serializers.CharField(max_length = 200, write_only = True)
    class Meta :
        model = Event
        fields = ['event_name', 'date', 'price','location','id','event_image','time','start_date','start_time', 'capacity','event_category']
        
    
    def to_representation(self, instance):
        data =  super().to_representation(instance)
        data['event_image'] = f'http://localhost:8000{instance.event_image.url}'
        return data
    
