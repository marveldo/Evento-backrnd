from rest_framework import serializers
from .models import User,DeviceInfo
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from .auth_utils import Google,register_social_auth_user
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from events.models import Event
from events.serializers import EventSerializer
from django.utils import timezone
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.core.files.storage import default_storage
import uuid
import os


today = timezone.now().date()

class Userserializer(serializers.ModelSerializer):
    upcoming_events_count = serializers.SerializerMethodField()
    past_events_count = serializers.SerializerMethodField()
    created_events_count = serializers.SerializerMethodField()
    upcoming_events = serializers.SerializerMethodField()
    profile_pic = serializers.ImageField(write_only = True, required=False)
    
    class Meta: 
        model = User
        fields = ['id','full_name','email','password','profile_img','upcoming_events_count', 'past_events_count', 'created_events_count', 'upcoming_events', 'location', 'profile_pic', 'website', 'instagram', 'facebook', 'twitter', 'bio']
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
        request = self.context.get('request')
        upcoming_events = Event.objects.filter(users = obj , start_date__gte = today  )
        serializer = EventSerializer(upcoming_events , many = True, context={'request':request})
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
    
    def update(self, instance : User, validated_data):
        image = validated_data.pop('profile_pic', None)
        password = validated_data.pop('password', None)

        for name , value in validated_data.items():
            setattr(instance , name , value)

        if password is not None :
            instance.set_password(password)

        if image is not None :
            extension = os.path.splitext(image.name)[1] 
            unique_filename = f"{uuid.uuid4().hex}{extension}" 
            file_path = default_storage.save(f'images/user/{unique_filename}', image)
            instance.profile_img = default_storage.url(file_path)
        
        instance.save()

        return instance
            

    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        device_id = self.context.get('device_id')
        if device_id is None :
            return data
        data['device_id'] = device_id
        return data
    
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
    
class LogoutSerializer(serializers.Serializer):
    device_id = serializers.CharField(required = True)
    refresh_token = serializers.CharField(required = True)

    def validate(self, attrs):
        refresh = attrs.get('refresh_token')
        device_id = attrs.get('device_id')

        
        try:
            refresh_derived = RefreshToken(refresh)
        except TokenError :
            refresh_derived = None
            raise serializers.ValidationError(detail='Token has been blacklisted', code=401)
        if refresh_derived is not None :
            refresh_derived.blacklist()
        try:
           device = DeviceInfo.objects.get(id = device_id)
        except DeviceInfo.DoesNotExist :
            device = None
        if device is not None :
            device.delete()
        
        return {}
    
class DeviceSerializer(serializers.ModelSerializer):

    class Meta :
        model = DeviceInfo
        exclude = ['access_token', 'refresh_token']
    

    