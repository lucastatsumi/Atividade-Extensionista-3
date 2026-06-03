from django.urls import path
from . import views

app_name = 'escola'

urlpatterns = [
    # Serie URLs
    path('series/', views.SerieListView.as_view(), name='serie_list'),
    path('series/create/', views.SerieCreateView.as_view(), name='serie_create'),
    path('series/<int:pk>/edit/', views.SerieUpdateView.as_view(), name='serie_update'),
    path('series/<int:pk>/delete/', views.SerieDeleteView.as_view(), name='serie_delete'),
    
    # Disciplina URLs
    path('disciplinas/', views.DisciplinaListView.as_view(), name='disciplina_list'),
    path('disciplinas/create/', views.DisciplinaCreateView.as_view(), name='disciplina_create'),
    path('disciplinas/<int:pk>/edit/', views.DisciplinaUpdateView.as_view(), name='disciplina_update'),
    path('disciplinas/<int:pk>/delete/', views.DisciplinaDeleteView.as_view(), name='disciplina_delete'),
    
    # Turma URLs
    path('turmas/', views.TurmaListView.as_view(), name='turma_list'),
    path('turmas/create/', views.TurmaCreateView.as_view(), name='turma_create'),
    path('turmas/<int:pk>/edit/', views.TurmaUpdateView.as_view(), name='turma_update'),
    path('turmas/<int:pk>/delete/', views.TurmaDeleteView.as_view(), name='turma_delete'),
]

