# EduPresence — Documento Técnico de Arquitetura (MVP)

## 1) Arquitetura completa do sistema

**Padrão:** Django MVT + serviços por domínio.

**Camadas:**
- **Apresentação:** Django Templates + Bootstrap 5 + JS Vanilla.
- **Aplicação:** Views baseadas em classe (CBV), Forms, validações, regras de permissão.
- **Domínio:** Models e serviços (cálculo de frequência/alerta).
- **Dados:** SQLite3.

**Apps Django (organização por domínio):**
- `core`: dashboard, home, utilitários, filtros de template.
- `accounts`: autenticação, perfis e permissões.
- `escola`: séries, turmas, disciplinas.
- `alunos`: cadastro, edição, inativação e matrícula.
- `frequencia`: chamada diária e histórico.
- `monitoramento`: cálculos de frequência e alertas de evasão.
- `relatorios`: relatórios por aluno/turma e exportação Excel.

## 2) Estrutura de pastas Django

```text
edupresence/
├── manage.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── core/
│   ├── accounts/
│   ├── escola/
│   ├── alunos/
│   ├── frequencia/
│   ├── monitoramento/
│   └── relatorios/
├── templates/
│   ├── base.html
│   ├── components/
│   └── dashboards/
├── static/
│   ├── css/
│   └── js/
└── requirements.txt
```

## 3) Modelos Django

```python
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        COORDENADOR = "COORD", "Coordenador"
        PROFESSOR = "PROF", "Professor"

    role = models.CharField(max_length=10, choices=Role.choices)


class Serie(models.Model):
    nome = models.CharField(max_length=50, unique=True)


class Turma(models.Model):
    nome = models.CharField(max_length=50)
    serie = models.ForeignKey(Serie, on_delete=models.PROTECT, related_name="turmas")


class Disciplina(models.Model):
    nome = models.CharField(max_length=100, unique=True)


class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="professor")


class Aluno(models.Model):
    class Status(models.TextChoices):
        ATIVO = "ATIVO", "Ativo"
        INATIVO = "INATIVO", "Inativo"

    nome = models.CharField(max_length=150)
    data_nascimento = models.DateField()
    responsavel = models.CharField(max_length=150)
    telefone = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ATIVO)


class Matricula(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.PROTECT, related_name="matriculas")
    turma = models.ForeignKey(Turma, on_delete=models.PROTECT, related_name="matriculas")
    data_matricula = models.DateField(auto_now_add=True)


class Frequencia(models.Model):
    class Status(models.TextChoices):
        PRESENTE = "P", "Presente"
        AUSENTE = "A", "Ausente"
        JUSTIFICADA = "J", "Falta justificada"

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="frequencias")
    turma = models.ForeignKey(Turma, on_delete=models.PROTECT, related_name="frequencias")
    data = models.DateField()
    status = models.CharField(max_length=1, choices=Status.choices)

    class Meta:
        unique_together = ("aluno", "turma", "data")


class AlertaEvasao(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="alertas")
    percentual_frequencia = models.DecimalField(max_digits=5, decimal_places=2)
    data_alerta = models.DateField(auto_now_add=True)
```

## 4) Views (CBV)

- `LoginView` e `LogoutView` (accounts).
- CRUD por CBVs (`ListView`, `CreateView`, `UpdateView`, `DetailView`) para Série, Turma, Disciplina e Aluno.
- `AlunoInativarView` (`UpdateView`).
- `MatriculaCreateView`.
- `ChamadaDiariaView` (`FormView`) com registro rápido da turma inteira.
- `HistoricoFrequenciaAlunoView` (`ListView`, paginada).
- `DashboardView` (`TemplateView`) com indicadores.
- `AlunosRiscoListView` (`ListView`) no monitoramento.
- Relatórios: `RelatorioAlunoView`, `RelatorioTurmaView`, `ExportarExcelView`.

**Boas práticas aplicadas:** `LoginRequiredMixin`, `PermissionRequiredMixin`, `SuccessMessageMixin`, `ModelForm`, paginação padrão.

## 5) URLs

```python
# config/urls.py
urlpatterns = [
    path("", include("apps.core.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("escola/", include("apps.escola.urls")),
    path("alunos/", include("apps.alunos.urls")),
    path("frequencia/", include("apps.frequencia.urls")),
    path("monitoramento/", include("apps.monitoramento.urls")),
    path("relatorios/", include("apps.relatorios.urls")),
]
```

## 6) Templates

- `templates/base.html`: layout principal (navbar + sidebar por perfil).
- `templates/accounts/login.html`.
- `templates/escola/*` (listas e formulários).
- `templates/alunos/*` (cadastro, edição, matrícula, inativação).
- `templates/frequencia/chamada_diaria.html` e `historico.html`.
- `templates/monitoramento/alunos_risco.html`.
- `templates/dashboards/home.html` com cards e gráfico mensal.
- `templates/relatorios/aluno.html` e `turma.html`.

## 7) Casos de uso

1. **Professor realiza chamada diária**: seleciona turma/data → marca status em lote → salva.
2. **Coordenador monitora risco**: acessa lista de alunos com frequência < 75%.
3. **Administrador gerencia professores**: cria usuário com papel PROFESSOR e permissões.
4. **Coordenação gera relatório**: filtra turma/aluno e exporta em Excel.

## 8) Fluxo de navegação

```text
Login
 └── Dashboard
     ├── Escola (Séries/Turmas/Disciplinas)
     ├── Alunos (Cadastro/Editar/Inativar/Matrícula)
     ├── Frequência (Chamada/Historico)
     ├── Monitoramento (Alunos em risco)
     └── Relatórios (Aluno/Turma/Excel)
```

## 9) Wireframes (texto)

```text
[Login]
+-------------------------+
| Usuário  [___________]  |
| Senha    [___________]  |
| [ Entrar ]              |
+-------------------------+

[Dashboard]
+---------------------------------------------------+
| Cards: Alunos | Turmas | Frequência Média | Risco |
| ------------------------------------------------- |
| Gráfico de Frequência Mensal                      |
| Lista rápida de alunos em risco                   |
+---------------------------------------------------+

[Chamada Diária]
+---------------------------------------------------+
| Turma [v] Data [__/__/____] [Carregar]            |
| Aluno 1 ( ) Presente ( ) Ausente ( ) Justificada  |
| Aluno 2 ( ) Presente ( ) Ausente ( ) Justificada  |
| ...                                                |
| [Marcar turma como presente] [Salvar chamada]      |
+---------------------------------------------------+
```

## 10) Roadmap MVP

- **MVP 1:** autenticação + perfis + cadastro escolar (série/turma/disciplina).
- **MVP 2:** cadastro/inativação de alunos + matrícula.
- **MVP 3:** chamada diária + histórico de frequência.
- **MVP 4:** dashboard + risco de evasão + relatórios + exportação Excel.

## 11) Cronograma (4 semanas)

- **Semana 1:** setup Django 5, app `accounts`, permissões, app `escola`.
- **Semana 2:** app `alunos` e `matriculas`, validações e mensagens.
- **Semana 3:** app `frequencia` (chamada em lote, histórico, paginação).
- **Semana 4:** monitoramento (<75%), dashboard com gráfico mensal, relatórios e exportação Excel, testes finais e homologação.

## Requisitos técnicos e práticas adotadas

- Python 3.12, Django 5, SQLite3.
- Frontend com Django Templates + Bootstrap 5 + JS Vanilla.
- Django Authentication (`LoginView`, `LogoutView`, permissões por grupo/papel).
- CBVs em todos os módulos de gestão.
- `ModelForm` para formulários e `messages` para feedback ao usuário.
- Paginação para listas (alunos, histórico e alertas).
- Serviço de cálculo de frequência:
  - `percentual = (presenças + justificadas) / total_aulas * 100`
  - alerta automático quando `< 75%`.
