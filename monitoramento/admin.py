from django.contrib import admin
from .models import AlertaEvasao


@admin.register(AlertaEvasao)
class AlertaEvasaoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'percentual_frequencia', 'severidade', 'resolvido', 'data_alerta')
    list_filter = ('severidade', 'resolvido', 'data_alerta')
    search_fields = ('aluno__nome',)
    ordering = ['-data_alerta']

