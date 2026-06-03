"""
Frequency calculation and monitoring services
"""
from decimal import Decimal
from django.db.models import Q, Count
from django.utils import timezone
from frequencia.models import Frequencia
from alunos.models import Aluno, Matricula
from .models import AlertaEvasao


class FrequenciaService:
    """Service for frequency calculations and monitoring"""

    @staticmethod
    def calcular_frequencia_aluno(aluno, turma=None, data_inicio=None, data_fim=None):
        """
        Calculate frequency percentage for a student
        
        Args:
            aluno: Aluno instance
            turma: Turma instance (optional - filters by turma)
            data_inicio: Start date for filtering (optional)
            data_fim: End date for filtering (optional)
        
        Returns:
            Frequency percentage (0-100) or None if no records
        """
        queryset = Frequencia.objects.filter(aluno=aluno)
        
        if turma:
            queryset = queryset.filter(turma=turma)
        
        if data_inicio:
            queryset = queryset.filter(data__gte=data_inicio)
        
        if data_fim:
            queryset = queryset.filter(data__lte=data_fim)
        
        total_aulas = queryset.count()
        
        if total_aulas == 0:
            return None
        
        presencas = queryset.filter(status='P').count()
        justificadas = queryset.filter(status='J').count()
        
        percentual = Decimal((presencas + justificadas) * 100) / Decimal(total_aulas)
        return float(percentual.quantize(Decimal('0.00')))

    @staticmethod
    def calcular_frequencia_turma(turma, data_inicio=None, data_fim=None):
        """
        Calculate average frequency for a class
        
        Args:
            turma: Turma instance
            data_inicio: Start date for filtering (optional)
            data_fim: End date for filtering (optional)
        
        Returns:
            Average frequency percentage or None if no records
        """
        queryset = Frequencia.objects.filter(turma=turma)
        
        if data_inicio:
            queryset = queryset.filter(data__gte=data_inicio)
        
        if data_fim:
            queryset = queryset.filter(data__lte=data_fim)
        
        if not queryset.exists():
            return None
        
        total_aulas = queryset.values('aluno').annotate(count=Count('id')).count()
        
        if total_aulas == 0:
            return None
        
        presencas = queryset.filter(status='P').count()
        justificadas = queryset.filter(status='J').count()
        total_registros = queryset.count()
        
        if total_registros == 0:
            return None
        
        percentual = Decimal((presencas + justificadas) * 100) / Decimal(total_registros)
        return float(percentual.quantize(Decimal('0.00')))

    @staticmethod
    def gerar_alertas_risco(turma=None, data_limite_percentual=75):
        """
        Generate alerts for students at risk of dropout
        
        Args:
            turma: Turma instance (optional - generates for all if None)
            data_limite_percentual: Frequency threshold for alert (default 75%)
        
        Returns:
            List of generated alerts
        """
        alertas_criados = []
        
        if turma:
            matriculas = Matricula.objects.filter(turma=turma, status='ATIVA')
        else:
            matriculas = Matricula.objects.filter(status='ATIVA')
        
        for matricula in matriculas:
            aluno = matricula.aluno
            frequencia = FrequenciaService.calcular_frequencia_aluno(aluno, turma=turma if turma else None)
            
            if frequencia is not None and frequencia < data_limite_percentual:
                severidade = AlertaEvasao.calcular_severidade(frequencia)
                
                # Check if alert already exists and is not resolved
                alerta_existente = AlertaEvasao.objects.filter(
                    aluno=aluno,
                    resolvido=False
                ).first()
                
                if alerta_existente:
                    # Update existing alert
                    alerta_existente.percentual_frequencia = Decimal(str(frequencia))
                    alerta_existente.severidade = severidade
                    alerta_existente.save()
                    alertas_criados.append(alerta_existente)
                else:
                    # Create new alert
                    alerta = AlertaEvasao.objects.create(
                        aluno=aluno,
                        percentual_frequencia=Decimal(str(frequencia)),
                        severidade=severidade
                    )
                    alertas_criados.append(alerta)
            else:
                # Mark alerts as resolved if frequency is now acceptable
                AlertaEvasao.objects.filter(
                    aluno=aluno,
                    resolvido=False
                ).update(
                    resolvido=True,
                    data_resolucao=timezone.now()
                )
        
        return alertas_criados

    @staticmethod
    def obter_alunos_em_risco(turma=None, percentual_minimo=75):
        """
        Get students at risk of dropout
        
        Args:
            turma: Turma instance (optional)
            percentual_minimo: Minimum frequency threshold
        
        Returns:
            QuerySet of Aluno objects at risk
        """
        # Get active alerts
        alertas = AlertaEvasao.objects.filter(
            resolvido=False,
            percentual_frequencia__lt=percentual_minimo
        )
        
        if turma:
            # Filter by students in the turma
            alunos_turma = Aluno.objects.filter(
                matriculas__turma=turma,
                matriculas__status='ATIVA'
            )
            alertas = alertas.filter(aluno__in=alunos_turma)
        
        return alertas.select_related('aluno').order_by('-percentual_frequencia')
