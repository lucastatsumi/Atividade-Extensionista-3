from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from accounts.mixins import CoordenadorRequiredMixin, AdminRequiredMixin
from .models import Aluno, Matricula
from .forms import AlunoForm, MatriculaForm


# CRUD for Aluno
class AlunoListView(CoordenadorRequiredMixin, ListView):
    model = Aluno
    template_name = 'alunos/aluno_list.html'
    context_object_name = 'alunos'
    paginate_by = 20


class AlunoDetailView(CoordenadorRequiredMixin, DetailView):
    model = Aluno
    template_name = 'alunos/aluno_detail.html'
    context_object_name = 'aluno'


class AlunoCreateView(CoordenadorRequiredMixin, SuccessMessageMixin, CreateView):
    model = Aluno
    form_class = AlunoForm
    template_name = 'alunos/aluno_form.html'
    success_url = reverse_lazy('alunos:aluno_list')
    success_message = 'Aluno criado com sucesso!'


class AlunoUpdateView(CoordenadorRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Aluno
    form_class = AlunoForm
    template_name = 'alunos/aluno_form.html'
    success_url = reverse_lazy('alunos:aluno_list')
    success_message = 'Aluno atualizado com sucesso!'


class AlunoInativarView(CoordenadorRequiredMixin, SuccessMessageMixin, UpdateView):
    """View to inactivate a student"""
    model = Aluno
    fields = []
    template_name = 'alunos/aluno_confirm_inativar.html'
    success_url = reverse_lazy('alunos:aluno_list')
    success_message = 'Aluno inativado com sucesso!'

    def form_valid(self, form):
        self.object.status = Aluno.Status.INATIVO
        return super().form_valid(form)


class AlunoDeleteView(AdminRequiredMixin, DeleteView):
    model = Aluno
    template_name = 'alunos/aluno_confirm_delete.html'
    success_url = reverse_lazy('alunos:aluno_list')
    success_message = 'Aluno deletado com sucesso!'


# CRUD for Matricula
class MatriculaListView(CoordenadorRequiredMixin, ListView):
    model = Matricula
    template_name = 'alunos/matricula_list.html'
    context_object_name = 'matriculas'
    paginate_by = 20


class MatriculaCreateView(CoordenadorRequiredMixin, SuccessMessageMixin, CreateView):
    model = Matricula
    form_class = MatriculaForm
    template_name = 'alunos/matricula_form.html'
    success_url = reverse_lazy('alunos:matricula_list')
    success_message = 'Matrícula criada com sucesso!'


class MatriculaUpdateView(CoordenadorRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Matricula
    form_class = MatriculaForm
    template_name = 'alunos/matricula_form.html'
    success_url = reverse_lazy('alunos:matricula_list')
    success_message = 'Matrícula atualizada com sucesso!'


class MatriculaDeleteView(AdminRequiredMixin, DeleteView):
    model = Matricula
    template_name = 'alunos/matricula_confirm_delete.html'
    success_url = reverse_lazy('alunos:matricula_list')
    success_message = 'Matrícula deletada com sucesso!'

