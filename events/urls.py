from django.urls import path
from .views import *

urlpatterns = [
    path('',EventViewset.as_view({'get':'list', 'post':'create'})),
]