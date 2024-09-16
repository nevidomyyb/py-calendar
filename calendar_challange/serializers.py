from rest_framework import serializers as sz
from calendar_challange.models import Evento
from django.utils import timezone
from datetime import datetime
from django.apps import apps
from django.conf import settings
import django_filters

class EventoFilter(django_filters.FilterSet):
    
    idevento = django_filters.NumberFilter(field_name='idevento')
    data_inicio = django_filters.DateFilter(field_name='data', lookup_expr='gte')
    data_fim = django_filters.DateFilter(field_name='data', lookup_expr='lte')
    titulo = django_filters.CharFilter(field_name='titulo', lookup_expr='icontains')
    
    class Meta:
        model = Evento
        fields = ['idevento', 'data', 'titulo']
    

class EventoSerializer(sz.ModelSerializer):
    
    class Meta:
        model = Evento
        fields = ['idevento', 'titulo', 'descricao', 'data', 'horario']
    
    def _get_data_horario_inicio(self, validated_data):
        if validated_data['data'] and validated_data['horario']:
            naive_datetime = datetime.combine(validated_data['data'], validated_data['horario'])
        elif validated_data['data']:
            endtime = datetime.strptime(settings.DEFAULT_HOUR, settings.DEFAULT_HOUR_FORMAT).time()
            naive_datetime = datetime.combine(validated_data['data'], endtime)
        else:
            naive_datetime = datetime.now()
        aware_datetime = timezone.make_aware(naive_datetime, timezone.get_current_timezone())
        return aware_datetime.strftime('%Y-%m-%dT%H:%M:%S%z'), aware_datetime
    
    def create(self, validated_data: dict):
        app = apps.get_app_config('calendar_challange')
        service = app.servico_calendario
        datetime_str_inicio, datetime_inicio = self._get_data_horario_inicio(validated_data)
        validated_data['data'] = datetime_inicio.date()
        validated_data['horario'] = datetime_inicio.time()
        tarefa = {
            'summary': validated_data['titulo'],
            'description': validated_data['descricao'],
            'start': {
                'dateTime': datetime_str_inicio,
                'timeZone': 'America/Sao_Paulo',
            },
            'end': {
                'dateTime': datetime_str_inicio,
                'timeZone': 'America/Sao_Paulo',
            },
            'reminders': {
                'useDefault': True
            }
        }   
        event = service.events().insert(calendarId=settings.DEFAULT_CALENDAR_ID, body=tarefa).execute()
        validated_data['idevento_calendar'] = event['id']
        obj = super().create(validated_data)
        return obj