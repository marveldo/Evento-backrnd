from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from .auth_utils import Google,register_social_auth_user
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from events.models import Event
from events.serializers import EventSerializer
from django.utils import timezone

today = timezone.now().date()

class Userserializer(serializers.ModelSerializer):
    upcoming_events_count = serializers.SerializerMethodField()
    past_events_count = serializers.SerializerMethodField()
    created_events_count = serializers.SerializerMethodField()
    upcoming_events = serializers.SerializerMethodField()
    
    class Meta: 
        model = User
        fields = ['id','full_name','email','password','profile_img','upcoming_events_count', 'past_events_count', 'created_events_count', 'upcoming_events']
        extra_kwargs = {'password': {'write_only':True}, '*':{'required': False}}
    
    def get_upcoming_events_count(self, obj : User) :
        """Get the count of a Users Upcoming events (Events later than today) into the serializer methodfield

        Args:
            obj (User): User Model

        Returns:
            int : Count of the upcoming events
        """
        count = Event.objects.filter(users = obj , start_date__gte = today  ).count()
        return count
    
    def get_past_events_count(self, obj : User):
        """Get the count of the past Events of a user(Events Before Today) into the serializer methodfield

        Args:
            obj (User): The User Model

        Returns:
            int : Count of the users past event
        """
        count = Event.objects.filter(users = obj , start_date__lt = today  ).count()
        return count
    
    def get_created_events_count(self, obj : User):
        """Get the count of the Users created events for the serializer methodField

        Args:
            obj (User): User Model

        Returns:
            int : Count of Users Created events
        """
        count = Event.objects.filter(created_by = obj.email).count()
        return count
    
    def get_upcoming_events(self, obj : User) :
        """Returns the users Upcoming events

        Args:
            obj (User): The User model

        Returns:
            _type_: serialized data
        """
        upcoming_events = Event.objects.filter(users = obj , start_date__gte = today  )
        serializer = EventSerializer(upcoming_events , many = True)
        return serializer.data

    def validate(self, attrs):
        if not self.instance and not attrs.get('full_name'):
            raise serializers.ValidationError({'full_name':'Field Cannot be empty'})
        if not self.instance and not attrs.get('email'):
            raise serializers.ValidationError({'email':'Field Cannot be empty'})
        if not self.instance and not attrs.get('password'):
            raise serializers.ValidationError({'password':'Password cannot be empty'})
        return super().validate(attrs)
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(
            **validated_data
        )
        user.set_password(password)
        user.save()
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
          "no_active_account": {
              'status_code' : status.HTTP_401_UNAUTHORIZED,
              'message' : 'Not Authorized'
          }
    }

class GoogleSigninSerializer(serializers.Serializer):
    
    access_token = serializers.CharField(min_length=6)

    def validate_access_token(self,access_token):
        google_user_data = Google.validate(access_token)
        try:
            user_id = google_user_data['sub']
        except:
            raise serializers.ValidationError('Something is wrong with the token')
        
        if google_user_data['aud'] != settings.GOOGLE_CLIENT_ID :
            raise AuthenticationFailed(detail='could not verify user')
        email = google_user_data['email']
        picture = google_user_data['picture']
        full_name = f"{google_user_data['given_name']} {google_user_data['family_name']}"
        provider = 'google'
        return register_social_auth_user(provider=provider , email=email, full_name=full_name, picture=picture)