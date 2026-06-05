from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.db.models import Count, Q
from accounts.mixins import CoordenadorRequiredMixin
from .models import AlertaEvasao
from .services import FrequenciaService
from escola.models import Turma
from alunos.models import Aluno


class AlunosRiscoListView(CoordenadorRequiredMixin, ListView):
    """List of students at risk of dropout"""
    model = AlertaEvasao
    template_name = 'monitoramento/alunos_risco.html'
    context_object_name = 'alertas'
    paginate_by = 20

    def get_queryset(self):
        queryset = AlertaEvasao.objects.filter(resolvido=False)
        
        # Filter by turma if provided
        turma_id = self.request.GET.get('turma')
        if turma_id:
            from alunos.models import Aluno
            alunos_turma = Aluno.objects.filter(
                matriculas__turma_id=turma_id,
                matriculas__status='ATIVA'
            )
            queryset = queryset.filter(aluno__in=alunos_turma)
        
        # Filter by severity if provided
        severidade = self.request.GET.get('severidade')
        if severidade:
            queryset = queryset.filter(severidade=severidade)
        
        return queryset.select_related('aluno').order_by('-percentual_frequencia')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['turmas'] = Turma.objects.filter(ativo=True)
        context['severidades'] = AlertaEvasao.Severidade.choices
        context['turma_filtro'] = self.request.GET.get('turma', '')
        context['severidade_filtro'] = self.request.GET.get('severidade', '')
        return context


class DashboardMonitoramentoView(CoordenadorRequiredMixin, TemplateView):
    """Monitoring dashboard view"""
    template_name = 'monitoramento/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Total students and classes
        context['total_alunos'] = Aluno.objects.filter(status='ATIVO').count()
        context['total_turmas'] = Turma.objects.filter(ativo=True).count()
        
        # Total students at risk
        alertas_ativos = AlertaEvasao.objects.filter(resolvido=False)
        context['total_risco'] = alertas_ativos.count()
        context['alertas_alta'] = alertas_ativos.filter(severidade='ALTA').count()
        context['alertas_media'] = alertas_ativos.filter(severidade='MEDIA').count()
        
        # Generate alerts if needed
        FrequenciaService.gerar_alertas_risco()
        
        # Students resolved
        context['alertas_resolvidos'] = AlertaEvasao.objects.filter(resolvido=True).count()
        
        # Recent alerts
        context['alertas_recentes'] = alertas_ativos.select_related('aluno')[:10]
        
        return context

