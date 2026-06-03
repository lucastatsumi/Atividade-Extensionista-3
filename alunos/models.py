from django.db import models
from escola.models import Turma


class Aluno(models.Model):
    """Students"""
    
    class Status(models.TextChoices):
        ATIVO = "ATIVO", "Ativo"
        INATIVO = "INATIVO", "Inativo"

    nome = models.CharField(max_length=150, verbose_name="Nome do Aluno")
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    responsavel = models.CharField(max_length=150, verbose_name="Responsável")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    email = models.EmailField(blank=True, verbose_name="Email")
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ATIVO,
        verbose_name="Status"
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"
        ordering = ['nome']

    def __str__(self):
        return self.nome

    @property
    def idade(self):
        from datetime import date
        today = date.today()
        return today.year - self.data_nascimento.year - ((today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day))


class Matricula(models.Model):
    """Student enrollment"""
    
    class Status(models.TextChoices):
        ATIVA = "ATIVA", "Ativa"
        CANCELADA = "CANCELADA", "Cancelada"
        TRANSFERIDA = "TRANSFERIDA", "Transferida"

    aluno = models.ForeignKey(Aluno, on_delete=models.PROTECT, related_name="matriculas", verbose_name="Aluno")
    turma = models.ForeignKey(Turma, on_delete=models.PROTECT, related_name="matriculas", verbose_name="Turma")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ATIVA,
        verbose_name="Status"
    )
    data_matricula = models.DateField(auto_now_add=True, verbose_name="Data de Matrícula")
    data_cancelamento = models.DateField(null=True, blank=True, verbose_name="Data de Cancelamento")
    observacoes = models.TextField(blank=True, verbose_name="Observações")

    class Meta:
        verbose_name = "Matrícula"
        verbose_name_plural = "Matrículas"
        ordering = ['aluno', 'turma']
        unique_together = ('aluno', 'turma')

    def __str__(self):
        return f"{self.aluno.nome} - {self.turma.nome}"

