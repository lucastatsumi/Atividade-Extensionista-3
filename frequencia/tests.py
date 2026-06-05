from datetime import date

from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from alunos.models import Aluno, Matricula
from escola.models import Serie, Turma
from frequencia.models import Frequencia


class ChamadaDiariaViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='professor',
            password='senha-forte',
            role=User.Role.PROFESSOR,
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
        self.aluno_ausente = Aluno.objects.create(
            nome='Aluno Ausente',
            data_nascimento=date(2018, 2, 10),
            responsavel='Responsável 2',
            telefone='2222-2222',
        )
        Matricula.objects.create(aluno=self.aluno_presente, turma=self.turma)
        Matricula.objects.create(aluno=self.aluno_ausente, turma=self.turma)

    def test_chamada_page_posts_turma_and_data_and_saves_statuses(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('frequencia:chamada_diaria'), {
            'turma': self.turma.id,
            'data': '2026-06-05',
            f'status_{self.aluno_presente.id}': 'P',
            f'status_{self.aluno_ausente.id}': 'A',
        })

        self.assertRedirects(
            response,
            f'{reverse("frequencia:chamada_diaria")}?turma={self.turma.id}&data=2026-06-05',
        )
        self.assertEqual(Frequencia.objects.count(), 2)
        self.assertEqual(
            Frequencia.objects.get(aluno=self.aluno_presente, turma=self.turma).status,
            'P',
        )
        self.assertEqual(
            Frequencia.objects.get(aluno=self.aluno_ausente, turma=self.turma).status,
            'A',
        )

    def test_chamada_page_renders_hidden_fields_and_bulk_marking_script(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('frequencia:chamada_diaria'), {
            'turma': self.turma.id,
            'data': '2026-06-05',
        })

        self.assertContains(response, f'name="turma" value="{self.turma.id}"')
        self.assertContains(response, 'name="data" value="2026-06-05"')
        self.assertContains(response, 'function marcarTodos(status)')
