from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import AUTH_HEADER_TYPES, TokenError , InvalidToken
from .serializers import *
from api.utils import success_response,error_validation,get_user_from_access_token
from .tasks import run_send_mail
from rest_framework.decorators import action
# Create your views here.



class HomeView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    
    def get(self,request):
        return success_response(status_code=200,message='welcome')

class UserPostViewset(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    """Class based View for creating and Updating a user

    Args:
        viewsets (_type_): GenericViewset for user
        mixins (_type_): mixins for creating models

    """
    queryset = User.objects.all()
    serializer_class = Userserializer
    
    def get_permissions(self):
        permission_classes = self.permission_classes
        
        match self.action :
            case 'me':
                permission_classes = [permissions.IsAuthenticated]
        
        return (permission() for permission in permission_classes)
    

    def create(self, request, *args, **kwargs):
        """Function that handles the Post request

        Args:
            request (_type_): argument that holds exception info of the user accessing it

        """
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
           self.perform_create(serializer=serializer)
           user = serializer.instance
           run_send_mail(user_id=str(user.id))
           return success_response(status_code=status.HTTP_201_CREATED,message='Registeration Successful',data=serializer.data)
        else :
            return error_validation(serializer=serializer, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
    def list(self, request, *args, **kwargs):
        users = self.get_queryset()
        serializer = self.get_serializer(users ,many = True)
        return success_response(
            status_code=200,
            message="succesfully listed",
            data= serializer.data
        )
    
    @action(methods=['get', 'put', 'delete'], detail=False)
    def me(self,request):
        match request.method :
            case 'GET':
                user = request.user
                serializer = self.get_serializer(user, many = False)
                return success_response(
                     status_code=200,
                     message='User Retrieved Successfully',
                     data=serializer.data
                )
         

class LoginUser(generics.GenericAPIView):
    """Class Based View to Login a user

    Args:
        generics (_type_): Generic api View

    """
    serializer_class = CustomTokenObtainPairSerializer


    def post(self,request):
        """This handles the post request and validations

        Args:
            request (_type_): Function that handles the post request

      
        """
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
           access_token = serializer.validated_data.get('access')
           refresh_token = serializer.validated_data.get('refresh')
           user = get_user_from_access_token(access_token=access_token)
           return success_response(
            status_code=status.HTTP_200_OK,
            message='Login Successful',
            access_token=access_token,
            refresh_token=refresh_token,
            data=user
           )
        else :
            return error_validation(serializer=serializer, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
class RefreshUser(generics.GenericAPIView):
    """Class Based View to handletoken refresh

    Args:
        generics (API View): Class Based View

   """
    serializer_class = TokenRefreshSerializer
    www_authenticate_realm = "api"
    def get_authenticate_header(self, request) -> str:
        return '{} realm="{}"'.format(
            AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )


    def post(self, request : Request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        try: 
            serializer.is_valid(raise_exception = True)
        except TokenError as e :
            raise InvalidToken(e.args[0])
        access_token = serializer.validated_data.get('access')
        refresh_token = serializer.validated_data.get('refresh')
        user = get_user_from_access_token(access_token=access_token)
        return success_response(
            status_code=status.HTTP_200_OK,
            message='Refresh Successful',
            access_token=access_token,
            refresh_token=refresh_token,
            data=user
        )

        

class GoogleSigninView(generics.GenericAPIView):
    """View for google sign in

    Args:
        generics (_type_): _description_
    """

    serializer_class = GoogleSigninSerializer

    def post(self,request):
        """function that handles post requests in the view

        Args:
            request (Request): description of backend requests
        """
       
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            access_token = serializer.validated_data['access_token']['access']
            refresh_token = serializer.validated_data['access_token']['refresh']
            status_code = serializer.validated_data['access_token']['status_code']
            user = get_user_from_access_token(access_token=access_token)
            return success_response(
            status_code=status_code,
            message='Login Successful',
            access_token=access_token,
            refresh_token=refresh_token,
            data=user
           )
        else:
            return error_validation(serializer=serializer, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

        
    



    

    
    

