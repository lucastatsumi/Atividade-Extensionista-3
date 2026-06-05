from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from alunos.models import Aluno, Matricula
from escola.models import Serie, Turma
from frequencia.models import Frequencia


class DashboardViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='coordenador',
            password='senha-forte',
            role=User.Role.COORDENADOR,
        )
        self.serie = Serie.objects.create(nome='1º Ano')
        self.turma = Turma.objects.create(
            nome='Turma A',
            serie=self.serie,
            ano=2026,
            periodo='MATUTINO',
        )
        self.aluno_presente = Aluno.objects.create(
            nome='Aluno Presente',
            data_nascimento=date(2018, 1, 10),
            responsavel='Responsável 1',
            telefone='1111-1111',
        )
        self.aluno_risco = Aluno.objects.create(
            nome='Aluno em Risco',
            data_nascimento=date(2018, 2, 10),
            responsavel='Responsável 2',
            telefone='2222-2222',
        )
        Matricula.objects.create(aluno=self.aluno_presente, turma=self.turma)
        Matricula.objects.create(aluno=self.aluno_risco, turma=self.turma)
        Frequencia.objects.create(
            aluno=self.aluno_presente,
            turma=self.turma,
            data=date(2026, 6, 1),
            status='P',
        )
        Frequencia.objects.create(
            aluno=self.aluno_risco,
            turma=self.turma,
            data=date(2026, 6, 1),
            status='A',
        )

    def test_dashboard_uses_database_values_in_summary_cards(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('core:dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_alunos'], 2)
        self.assertEqual(response.context['total_turmas'], 1)
        self.assertEqual(response.context['frequencia_media'], Decimal('50.00'))
        self.assertEqual(response.context['alunos_em_risco'], 1)
        self.assertContains(response, '2')
