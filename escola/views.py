from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from accounts.mixins import CoordenadorRequiredMixin, AdminRequiredMixin
from .models import Serie, Disciplina, Turma, Professor
from .forms import SerieForm, DisciplinaForm, TurmaForm, ProfessorForm
from alunos.models import Matricula, Aluno


# CRUD for Serie
class SerieListView(CoordenadorRequiredMixin, ListView):
    model = Serie
    template_name = 'escola/serie_list.html'
    context_object_name = 'series'
    paginate_by = 10


class SerieCreateView(CoordenadorRequiredMixin, SuccessMessageMixin, CreateView):
    model = Serie
    form_class = SerieForm
    template_name = 'escola/serie_form.html'
    success_url = reverse_lazy('escola:serie_list')
    success_message = 'Série criada com sucesso!'


class SerieUpdateView(CoordenadorRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Serie
    form_class = SerieForm
    template_name = 'escola/serie_form.html'
    success_url = reverse_lazy('escola:serie_list')
    success_message = 'Série atualizada com sucesso!'


class SerieDeleteView(AdminRequiredMixin, DeleteView):
    model = Serie
    template_name = 'escola/serie_confirm_delete.html'
    success_url = reverse_lazy('escola:serie_list')
    success_message = 'Série deletada com sucesso!'


# CRUD for Disciplina
class DisciplinaListView(CoordenadorRequiredMixin, ListView):
    model = Disciplina
    template_name = 'escola/disciplina_list.html'
    context_object_name = 'disciplinas'
    paginate_by = 10


class DisciplinaCreateView(CoordenadorRequiredMixin, SuccessMessageMixin, CreateView):
    model = Disciplina
    form_class = DisciplinaForm
    template_name = 'escola/disciplina_form.html'
    success_url = reverse_lazy('escola:disciplina_list')
    success_message = 'Disciplina criada com sucesso!'


class DisciplinaUpdateView(CoordenadorRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Disciplina
    form_class = DisciplinaForm
    template_name = 'escola/disciplina_form.html'
    success_url = reverse_lazy('escola:disciplina_list')
    success_message = 'Disciplina atualizada com sucesso!'


class DisciplinaDeleteView(AdminRequiredMixin, DeleteView):
    model = Disciplina
    template_name = 'escola/disciplina_confirm_delete.html'
    success_url = reverse_lazy('escola:disciplina_list')
    success_message = 'Disciplina deletada com sucesso!'


# CRUD for Turma
class TurmaListView(CoordenadorRequiredMixin, ListView):
    model = Turma
    template_name = 'escola/turma_list.html'
    context_object_name = 'turmas'
    paginate_by = 10


class TurmaDetailView(CoordenadorRequiredMixin, DetailView):
    model = Turma
    template_name = 'escola/turma_detail.html'
    context_object_name = 'turma'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all enrollments for this class, ordered by student name
        matriculas = Matricula.objects.filter(turma=self.object).select_related('aluno').order_by('aluno__nome')
        context['matriculas'] = matriculas
        context['total_alunos'] = matriculas.count()
        # Count active enrollments
        ativas = matriculas.filter(status='ATIVA').count()
        context['alunos_ativos'] = ativas
        return context


class TurmaCreateView(CoordenadorRequiredMixin, SuccessMessageMixin, CreateView):
    model = Turma
    form_class = TurmaForm
    template_name = 'escola/turma_form.html'
    success_url = reverse_lazy('escola:turma_list')
    success_message = 'Turma criada com sucesso!'


class TurmaUpdateView(CoordenadorRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Turma
    form_class = TurmaForm
    template_name = 'escola/turma_form.html'
    success_url = reverse_lazy('escola:turma_list')
    success_message = 'Turma atualizada com sucesso!'


class TurmaDeleteView(AdminRequiredMixin, DeleteView):
    model = Turma
    template_name = 'escola/turma_confirm_delete.html'
    success_url = reverse_lazy('escola:turma_list')
    success_message = 'Turma deletada com sucesso!'

