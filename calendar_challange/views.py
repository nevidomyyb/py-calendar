from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from calendar_challange.models import Evento
from calendar_challange.serializers import EventoSerializer, EventoFilter
from django.apps import apps
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from googleapiclient.errors import HttpError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
# Create your views here.

class ListCreateEvent(ListCreateAPIView):
    serializer_class = EventoSerializer
    queryset = Evento.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = EventoFilter
    search_fields = ['titulo']
    ordering_fields = ['data', 'titulo']
    
class RetrieveUpdateDestroyEvent(RetrieveUpdateDestroyAPIView):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    
    def destroy(self, request, pk):
        instance = self.get_queryset().get(pk=pk)
        app = apps.get_app_config('calendar_challange')
        service = app.servico_calendario
        response = {}
        try:
            service.events().delete(calendarId=settings.DEFAULT_CALENDAR_ID, eventId=instance.idevento_calendar).execute()
        except HttpError as e:
            instance.delete()
            response["google_error"] = e.error_details[0]['message']
            response["mensagem"] = "Apagar o evento no calendário não foi possível."
            return Response(response, status=status.HTTP_207_MULTI_STATUS)
        instance.delete()
        return Response(response, status=status.HTTP_204_NO_CONTENT)
        