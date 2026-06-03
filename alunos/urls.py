from django.urls import path
from . import views

app_name = 'alunos'

urlpatterns = [
    # Aluno URLs
    path('', views.AlunoListView.as_view(), name='aluno_list'),
    path('create/', views.AlunoCreateView.as_view(), name='aluno_create'),
    path('<int:pk>/', views.AlunoDetailView.as_view(), name='aluno_detail'),
    path('<int:pk>/edit/', views.AlunoUpdateView.as_view(), name='aluno_update'),
    path('<int:pk>/inativar/', views.AlunoInativarView.as_view(), name='aluno_inativar'),
    path('<int:pk>/delete/', views.AlunoDeleteView.as_view(), name='aluno_delete'),
    
    # Matricula URLs
    path('matriculas/', views.MatriculaListView.as_view(), name='matricula_list'),
    path('matriculas/create/', views.MatriculaCreateView.as_view(), name='matricula_create'),
    path('matriculas/<int:pk>/edit/', views.MatriculaUpdateView.as_view(), name='matricula_update'),
    path('matriculas/<int:pk>/delete/', views.MatriculaDeleteView.as_view(), name='matricula_delete'),
]

