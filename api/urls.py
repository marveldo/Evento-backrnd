from django.urls import path,include


urlpatterns = [
    path('auth/', include("users.urls")),
    path('events/', include('events.urls'))
]
