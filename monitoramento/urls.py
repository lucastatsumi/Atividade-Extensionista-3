from django.urls import path
from . import views

app_name = 'monitoramento'

urlpatterns = [
    path('dashboard/', views.DashboardMonitoramentoView.as_view(), name='dashboard'),
    path('alunos-risco/', views.AlunosRiscoListView.as_view(), name='alunos_risco'),
]

