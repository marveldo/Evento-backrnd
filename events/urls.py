from django.urls import path
from .views import *

urlpatterns = [
    path('',EventViewset.as_view({'get':'list', 'post':'create'})),
    path('<str:pk>/', EventViewset.as_view({'get': 'retrieve'})),
    path('<str:pk>/attendees/', EventViewset.as_view({'get': 'attendees' , 'post': 'attendees'}))
]
