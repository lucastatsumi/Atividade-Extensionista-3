from django.db import models
from alunos.models import Aluno
from escola.models import Turma


class Frequencia(models.Model):
    """Attendance records"""
    
    class Status(models.TextChoices):
        PRESENTE = "P", "Presente"
        AUSENTE = "A", "Ausente"
        JUSTIFICADA = "J", "Falta justificada"

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="frequencias", verbose_name="Aluno")
    turma = models.ForeignKey(Turma, on_delete=models.PROTECT, related_name="frequencias", verbose_name="Turma")
    data = models.DateField(verbose_name="Data")
    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        verbose_name="Status"
    )
    observacoes = models.TextField(blank=True, verbose_name="Observações")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Frequência"
        verbose_name_plural = "Frequências"
        ordering = ['-data', 'aluno']
        unique_together = ('aluno', 'turma', 'data')

    def __str__(self):
        return f"{self.aluno.nome} - {self.data} ({self.get_status_display()})"

    @property
    def apresentacao_status(self):
        """Display status in Portuguese"""
        return self.get_status_display()

