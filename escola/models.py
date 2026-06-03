from django.db import models
from accounts.models import User


class Serie(models.Model):
    """Academic series/grades (e.g., 1st, 2nd, 3rd year)"""
    nome = models.CharField(max_length=50, unique=True, verbose_name="Nome da Série")
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Série"
        verbose_name_plural = "Séries"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Disciplina(models.Model):
    """School subjects/disciplines"""
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome da Disciplina")
    codigo = models.CharField(max_length=10, unique=True, verbose_name="Código")
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    carga_horaria = models.IntegerField(default=60, verbose_name="Carga Horária")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Turma(models.Model):
    """Classes/Classrooms"""
    nome = models.CharField(max_length=50, verbose_name="Nome da Turma")
    serie = models.ForeignKey(Serie, on_delete=models.PROTECT, related_name="turmas", verbose_name="Série")
    ano = models.IntegerField(verbose_name="Ano Letivo")
    periodo = models.CharField(
        max_length=10,
        choices=[('MATUTINO', 'Matutino'), ('VESPERTINO', 'Vespertino'), ('NOTURNO', 'Noturno')],
        verbose_name="Período"
    )
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"
        ordering = ['serie', 'nome']
        unique_together = ('nome', 'serie', 'ano')

    def __str__(self):
        return f"{self.nome} ({self.serie.nome}) - {self.ano}"


class Professor(models.Model):
    """Teachers"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="professor", verbose_name="Usuário")
    disciplinas = models.ManyToManyField(Disciplina, related_name="professores", verbose_name="Disciplinas")
    turmas = models.ManyToManyField(Turma, related_name="professores", verbose_name="Turmas")
    numero_registro = models.CharField(max_length=20, unique=True, verbose_name="Número de Registro")
    telefone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Professor"
        verbose_name_plural = "Professores"
        ordering = ['user__first_name']

    def __str__(self):
        return self.user.get_full_name() or self.user.username

