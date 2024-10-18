from api.utils import CustomPagination
from rest_framework import viewsets
from rest_framework import mixins
from .models import Event,EventTag
from .serializers import EventSerializer
from rest_framework import status
from rest_framework.request import Request
from api.utils import error_validation,success_response
from rest_framework import permissions

# Create your views here.



class EventViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """View to get all events

    Args:
        viewsets (Model): Vieswets class being inherited

    
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]

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
        return queryset
    
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
            request (Request Object): Stralette Requests

        """
        events = self.get_queryset()
        page = self.paginate_queryset(events)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(data=serializer.data)
    
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
    
        

        
        
