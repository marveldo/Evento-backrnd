from .views import *
from django.urls import path

urlpatterns = [
    path('', HomeView.as_view()),
    path('register/',UserPostViewset.as_view({'post':'create'})),
    path('login/', LoginUser.as_view()),
    path('logout/', LogoutView.as_view()),
    path('google/',GoogleSigninView.as_view()),
    path('users/', UserPostViewset.as_view({'get':'list'})),
    path('refresh/', RefreshUser.as_view()),
    path('current-user/', UserPostViewset.as_view({'get':'me', 'put': 'me', 'delete':'me'})),
    path('devices/', DeviceView.as_view({'get':'list'})),
    path('logout-device/<str:pk>/', DeviceView.as_view({'delete': 'destroy'}))
]
