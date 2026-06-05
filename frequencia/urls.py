from django.urls import path
from . import views

app_name = 'frequencia'

urlpatterns = [
    path('chamada/', views.ChamadaDiariaView.as_view(), name='chamada_diaria'),
    path('historico/', views.HistoricoFrequenciaListView.as_view(), name='historico'),
    path('criar/', views.FrequenciaCreateView.as_view(), name='criar'),
    path('api/atualizar-status/', views.atualizar_status_presenca, name='atualizar_status'),
]

