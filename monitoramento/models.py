from django.db import models
from alunos.models import Aluno


class AlertaEvasao(models.Model):
    """Dropout risk alerts"""
    
    class Severidade(models.TextChoices):
        BAIXA = "BAIXA", "Baixa"
        MEDIA = "MEDIA", "Média"
        ALTA = "ALTA", "Alta"

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="alertas", verbose_name="Aluno")
    percentual_frequencia = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Percentual de Frequência"
    )
    severidade = models.CharField(
        max_length=10,
        choices=Severidade.choices,
        verbose_name="Severidade"
    )
    data_alerta = models.DateTimeField(auto_now_add=True, verbose_name="Data do Alerta")
    resolvido = models.BooleanField(default=False, verbose_name="Resolvido")
    data_resolucao = models.DateTimeField(null=True, blank=True, verbose_name="Data de Resolução")
    observacoes = models.TextField(blank=True, verbose_name="Observações")

    class Meta:
        verbose_name = "Alerta de Evasão"
        verbose_name_plural = "Alertas de Evasão"
        ordering = ['-data_alerta']

    def __str__(self):
        return f"Alerta {self.aluno.nome} - {self.get_severidade_display()}"

    @staticmethod
    def calcular_severidade(percentual):
        """Calculate alert severity based on frequency percentage"""
        if percentual >= 75:
            return None  # No alert
        elif percentual >= 50:
            return AlertaEvasao.Severidade.MEDIA
        else:
            return AlertaEvasao.Severidade.ALTA

