from django.apps import AppConfig
from .calendar_service import getCalendarService


class CalendarChallangeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'calendar_challange'

    def ready(self) -> None:
        self.servico_calendario = getCalendarService()
        print('Google Calendar service integrated and ready.')
        return super().ready()