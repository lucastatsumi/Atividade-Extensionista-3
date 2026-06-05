from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, FormView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from datetime import date
from accounts.mixins import ProfessorRequiredMixin
from .models import Frequencia
from .forms import FrequenciaForm, ChamadaDiariaForm


class ChamadaDiariaView(ProfessorRequiredMixin, FormView):
    """Daily attendance marking view"""
    template_name = 'frequencia/chamada_diaria.html'
    form_class = ChamadaDiariaForm
    success_url = reverse_lazy('frequencia:chamada_diaria')

    def form_valid(self, form):
        turma = form.cleaned_data['turma']
        data = form.cleaned_data['data']

        # Get POST data for attendance status
        matriculas = turma.matriculas.filter(status='ATIVA').select_related('aluno')
        registros_salvos = 0

        for matricula in matriculas:
            aluno = matricula.aluno
            status_key = f'status_{aluno.id}'
            status = self.request.POST.get(status_key, '')

            if status:
                Frequencia.objects.update_or_create(
                    aluno=aluno,
                    turma=turma,
                    data=data,
                    defaults={'status': status}
                )
                registros_salvos += 1

        if registros_salvos:
            messages.success(
                self.request,
                f'Chamada registrada com sucesso para {turma.nome} em {data.strftime("%d/%m/%Y")}. '
                f'{registros_salvos} registro(s) salvo(s).'
            )
        else:
            messages.warning(
                self.request,
                'Nenhum status foi selecionado para salvar a chamada.'
            )

        return redirect(
            f'{reverse("frequencia:chamada_diaria")}?turma={turma.id}&data={data.isoformat()}'
        )

    def form_invalid(self, form):
        messages.error(self.request, 'Não foi possível salvar a chamada. Verifique a turma e a data selecionadas.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from escola.models import Turma
        
        # Always include turmas for the form
        context['turmas'] = Turma.objects.filter(ativo=True)
        context['data_selecionada'] = date.today()

        # Check if turma and data are in request
        if self.request.method == 'POST' or ('turma' in self.request.GET and 'data' in self.request.GET):
            try:
                turma_id = self.request.POST.get('turma') or self.request.GET.get('turma')
                data_str = self.request.POST.get('data') or self.request.GET.get('data')

                context['turma_filtro'] = turma_id or ''

                if turma_id and data_str:
                    turma = Turma.objects.get(id=turma_id, ativo=True)
                    data_obj = date.fromisoformat(data_str)

                    matriculas = turma.matriculas.filter(status='ATIVA').select_related('aluno')
                    frequencias = {f.aluno_id: f for f in Frequencia.objects.filter(
                        turma=turma, data=data_obj
                    )}

                    context['turma_selecionada'] = turma
                    context['data_selecionada'] = data_obj
                    context['matriculas'] = matriculas
                    context['frequencias'] = frequencias
            except (Turma.DoesNotExist, ValueError):
                messages.error(self.request, 'Turma ou data inválida para carregar a chamada.')

        return context


class HistoricoFrequenciaListView(ProfessorRequiredMixin, ListView):
    """Attendance history view"""
    model = Frequencia
    template_name = 'frequencia/historico_frequencia.html'
    context_object_name = 'frequencias'
    paginate_by = 30

    def get_queryset(self):
        queryset = Frequencia.objects.all()
        
        # Filter by turma if provided
        turma_id = self.request.GET.get('turma')
        if turma_id:
            queryset = queryset.filter(turma_id=turma_id)
        
        # Filter by aluno if provided
        aluno_id = self.request.GET.get('aluno')
        if aluno_id:
            queryset = queryset.filter(aluno_id=aluno_id)
        
        # Filter by date range if provided
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')
        if data_inicio:
            queryset = queryset.filter(data__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data__lte=data_fim)
        
        return queryset.select_related('aluno', 'turma').order_by('-data', 'aluno')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from escola.models import Turma
        from alunos.models import Aluno
        
        context['turmas'] = Turma.objects.filter(ativo=True)
        context['alunos'] = Aluno.objects.filter(status='ATIVO')
        
        # Add filter values to context
        context['turma_filtro'] = self.request.GET.get('turma', '')
        context['aluno_filtro'] = self.request.GET.get('aluno', '')
        context['data_inicio'] = self.request.GET.get('data_inicio', '')
        context['data_fim'] = self.request.GET.get('data_fim', '')
        
        return context


class FrequenciaCreateView(ProfessorRequiredMixin, SuccessMessageMixin, CreateView):
    model = Frequencia
    form_class = FrequenciaForm
    template_name = 'frequencia/frequencia_form.html'
    success_url = reverse_lazy('frequencia:historico')
    success_message = 'Frequência registrada com sucesso!'

