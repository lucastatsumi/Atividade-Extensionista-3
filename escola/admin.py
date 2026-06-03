from django.contrib import admin
from .models import Serie, Disciplina, Turma, Professor


@admin.register(Serie)
class SerieAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ativo', 'criado_em')
    list_filter = ('ativo', 'criado_em')
    search_fields = ('nome',)
    ordering = ['nome']


@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo', 'carga_horaria', 'ativo', 'criado_em')
    list_filter = ('ativo', 'criado_em')
    search_fields = ('nome', 'codigo')
    ordering = ['nome']


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'serie', 'ano', 'periodo', 'ativo', 'criado_em')
    list_filter = ('serie', 'ano', 'periodo', 'ativo', 'criado_em')
    search_fields = ('nome',)
    ordering = ['serie', 'nome']


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'numero_registro', 'ativo', 'criado_em')
    list_filter = ('ativo', 'criado_em', 'disciplinas', 'turmas')
    search_fields = ('user__first_name', 'user__last_name', 'numero_registro')
    filter_horizontal = ('disciplinas', 'turmas')
    ordering = ['user__first_name']

    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Nome'

