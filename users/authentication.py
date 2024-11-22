from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import DeviceInfo

class UserJwtAuthentication(JWTAuthentication):

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None :
            return None
        
        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None
        decoded_token = raw_token.decode('utf-8')
        try :
            _ = DeviceInfo.objects.get(access_token = decoded_token)
        except DeviceInfo.DoesNotExist :
            return None
        
        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token) , validated_token
    

