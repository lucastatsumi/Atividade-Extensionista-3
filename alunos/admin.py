from django.contrib import admin
from .models import Aluno, Matricula


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_nascimento', 'responsavel', 'status', 'criado_em')
    list_filter = ('status', 'criado_em')
    search_fields = ('nome', 'responsavel')
    ordering = ['nome']


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'turma', 'status', 'data_matricula')
    list_filter = ('status', 'turma', 'data_matricula')
    search_fields = ('aluno__nome',)
    ordering = ['-data_matricula']

