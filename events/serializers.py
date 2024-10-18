from rest_framework import serializers
from .models import Event,EventTag



class EventSerializer(serializers.ModelSerializer):
    event_category = serializers.CharField(max_length = 200, write_only = True)
    class Meta :
        model = Event
        fields = ['event_name', 'date', 'price','location','event_image','id','time','start_date','start_time', 'capacity','event_category']
    
    def to_representation(self, instance):
        data =  super().to_representation(instance)
        data['event_image'] = f'http://localhost:8000{instance.event_image.url}'
        data['event_link'] = f'http://localhost:8000/api/v1/events/{instance.id}/'
        return data
    
    def create(self, validated_data):
        request = self.context.get('request')
        event_category = validated_data.pop('event_category')
        event = Event.objects.create(**validated_data)
        event.created_by = request.user.email
        event.save()
        event.users.add(request.user)
        eventtag , created = EventTag.objects.get_or_create(tag_name = event_category)
        
        event.tags.add(eventtag)
        return event
    
