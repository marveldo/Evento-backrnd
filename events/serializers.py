from rest_framework import serializers
from .models import Event,EventTag
from users.models import User

class Eventuserdetailserializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = ['id','full_name','email','profile_img']

class EventTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTag
        fields = '__all__'
        
class EventSerializer(serializers.ModelSerializer):
    event_category = serializers.CharField(max_length = 200, write_only = True)
    hosted_by = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta :
        model = Event
        fields = ['id','event_name', 'date','description', 'price','location','event_image','id','time','start_date','start_time', 'capacity','event_category','category','hosted_by']
    def get_category(self, obj : Event):
        tags = obj.tags.all()
        serializer = EventTagSerializer(tags , many = True)
        return serializer.data
    def get_hosted_by(self, obj : Event):
        """Returns the user that created the Event for the serializer methodfield

        Args:
            obj (Event): Event Obj

        Returns:
            _type_: serialized data
        """
        try :
            user = User.objects.get(email = obj.created_by)
            serializer = Eventuserdetailserializer(user, many = False)
            return serializer.data
        except User.DoesNotExist:
            return {}


    def to_representation(self, instance : Event):
        """Method for serializer representation

        Args:
            instance (Event): Event Object

        Returns:
            _type_: serialized data
        """
        data =  super().to_representation(instance)
        data['event_image'] = f'http://localhost:8000{instance.event_image.url}'
        data['event_link'] = f'http://localhost:3000/events/{instance.id}/'
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
    
