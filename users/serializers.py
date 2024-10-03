from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from .auth_utils import Google,register_social_auth_user
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


class Userserializer(serializers.ModelSerializer):

    class Meta: 
        model = User
        fields = ['id','full_name','email','password','profile_img']
        extra_kwargs = {'password': {'write_only':True}, '*':{'required': False}}

    
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