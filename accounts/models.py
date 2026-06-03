from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom User model with role-based access"""
    
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        COORDENADOR = "COORD", "Coordenador"
        PROFESSOR = "PROF", "Professor"

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.PROFESSOR
    )
    
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ['first_name']

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

