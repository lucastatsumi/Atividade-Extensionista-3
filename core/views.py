from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from alunos.models import Aluno, Matricula
from escola.models import Turma
from frequencia.models import Frequencia


class DashboardView(LoginRequiredMixin, TemplateView):
    """Main dashboard view"""
    template_name = 'core/dashboard.html'
    login_url = 'accounts:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard'

        total_frequencias = Frequencia.objects.count()
        total_presencas = Frequencia.objects.filter(status__in=['P', 'J']).count()
        frequencia_media = None

        if total_frequencias:
            frequencia_media = (
                Decimal(total_presencas * 100) / Decimal(total_frequencias)
            ).quantize(Decimal('0.01'))

        alunos_em_risco = 0
        alunos_processados = set()
        matriculas_ativas = Matricula.objects.filter(
            status='ATIVA',
            aluno__status='ATIVO',
        ).select_related('aluno')

        for matricula in matriculas_ativas:
            aluno_id = matricula.aluno_id
            if aluno_id in alunos_processados:
                continue

            registros_aluno = Frequencia.objects.filter(aluno_id=aluno_id)
            total_registros_aluno = registros_aluno.count()

            if not total_registros_aluno:
                continue

            presencas_aluno = registros_aluno.filter(status__in=['P', 'J']).count()
            percentual_aluno = (
                Decimal(presencas_aluno * 100) / Decimal(total_registros_aluno)
            )

            if percentual_aluno < Decimal('75'):
                alunos_em_risco += 1

            alunos_processados.add(aluno_id)

        context.update({
            'total_alunos': Aluno.objects.filter(status='ATIVO').count(),
            'total_turmas': Turma.objects.filter(ativo=True).count(),
            'frequencia_media': frequencia_media,
            'alunos_em_risco': alunos_em_risco,
        })
        return context
