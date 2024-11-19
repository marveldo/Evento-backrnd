from api.utils import CustomPagination
from rest_framework import viewsets
from rest_framework import mixins
from .models import Event,EventTag
from .serializers import EventSerializer
from users.serializers import Userserializer
from users.models import User,Notification
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.request import Request
from api.utils import error_validation,success_response
from rest_framework import permissions
from rest_framework import renderers

# Create your views here.



class EventViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    """View to get all events

    Args:
        viewsets (Model): Vieswets class being inherited

    
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes =[renderers.JSONRenderer]

    def get_queryset(self):
        """Alter defalult queryset

        Returns:
            Object: The queryset of the Model
        """
        queryset = super().get_queryset()
        if self.request.GET.get('tag'):
            event_tag = EventTag.objects.filter(tag_name__icontains=self.request.GET.get('tag')).first()
            if event_tag :
                return queryset.filter(tags = event_tag)
            elif self.request.GET.get('tag') == 'Recommended':
                user_city = self.request.user.location.split(",")[1].strip()
                return queryset.filter(location__icontains = user_city)
        return queryset
    
    @action(methods=['get','post'], detail=True)
    def attendees(self, request : Request, pk = None) :
        """Custom Action gotten to use with viewset

        Args:
            request (Request): request Object
            pk (_type_, optional): primary key value to get the object. Defaults to None.
        """
        
        match request.method :
            
            case 'GET':
              
              event = self.get_object()
              try:
                 event_creator = User.objects.get(email = event.created_by)
              except User.DoesNotExist :
                  return success_response(status_code=404, message='Detail Not Found')  
              attendees = event.users.exclude(id = event_creator.id)
              page = self.paginate_queryset(attendees)
              serializer = Userserializer(page, many = True, context={'request' : request}) 
              return self.get_paginated_response(data=serializer.data)  
            
            case 'POST':
                event = self.get_object()
                try :
                    user = User.objects.get(email = request.data.get('email'))
                    event_creator = User.objects.get(email = event.created_by)
                except User.DoesNotExist :
                    return success_response(status_code=404, message='Detail Not Found')
                if user in event.users.all():
                    return success_response(status_code=400, message='User Already registered')
                event.users.add(user)
                Notification.objects.create(
                    user = event_creator,
                    message= f'{user.email} just registered for your event'
                )
                attendees = event.users.exclude(id = event_creator.id) 
                page = self.paginate_queryset(attendees) 
                serializer = Userserializer(page, many = True, context={'request' : request}) 
                return self.get_paginated_response(data=serializer.data)  
                
                

    
    
    def get_paginated_response(self, data):
        """Function to overwrite the default pagination Function

        Args:
            data (dict): the serialized object

        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(status=status.HTTP_200_OK, message='Querysuccessful',data=data)

    def list(self, request : Request, *args, **kwargs):
        """function that handles the list view

        Args:
            request (Request Object): Http Requests

        """
        events = self.get_queryset()
        page = self.paginate_queryset(events)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(data=serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        """Function that handles the retrieve view with get a pk value

        Args:
            request (Request Object): Http request
        """
        event = self.get_object()
        serializer = self.get_serializer(event , many=False, context={'request':request})
        return success_response(
                       status_code=200,
                       message='Event Fetched Successfully',
                       data=serializer.data
                                )
    
    def create(self, request : Request, *args, **kwargs):
        """Function that handles the create view

        Args:
            request (Request): Http Request 

        """

        serializer = self.get_serializer(data = request.data , context = {'request' : request})
        if serializer.is_valid():
           self.perform_create(serializer=serializer)
           return success_response(status_code=status.HTTP_201_CREATED, 
                                   message='Event created',
                                   data=serializer.data
                                   )

        else :
            return error_validation(serializer=serializer , status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
        

        
        
