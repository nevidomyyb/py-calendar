from django.urls import path
from .views import ListCreateEvent, RetrieveUpdateDestroyEvent

app_name = "calendar_challange"

urlpatterns = [
    path('evento/', ListCreateEvent.as_view(), name='list-create-event'),
    path('evento/<int:pk>/', RetrieveUpdateDestroyEvent.as_view(), name='list-create-event'),
]
