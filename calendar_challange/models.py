from django.db import models

# Create your models here.
class Evento(models.Model):
    
    idevento = models.AutoField(primary_key=True)
    titulo = models.TextField(null=False, blank=False)
    descricao = models.TextField(null=True, blank=True)
    data = models.DateField(blank=True, null=True)
    horario = models.TimeField(null=True, blank=True)
    idevento_calendar = models.CharField(max_length=26, null=False)
    
    class Meta:
        db_table = "evento"
    
        