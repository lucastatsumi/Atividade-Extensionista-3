from django.contrib import admin
from .models import Frequencia


@admin.register(Frequencia)
class FrequenciaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'turma', 'data', 'status', 'criado_em')
    list_filter = ('status', 'turma', 'data', 'criado_em')
    search_fields = ('aluno__nome',)
    ordering = ['-data', 'aluno']

