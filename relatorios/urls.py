from django.urls import path
from . import views

app_name = 'relatorios'

urlpatterns = [
    path('aluno/', views.RelatorioAlunoView.as_view(), name='relatorio_aluno'),
    path('turma/', views.RelatorioTurmaView.as_view(), name='relatorio_turma'),
    path('exportar-excel/', views.ExportarExcelView.as_view(), name='exportar_excel'),
]

