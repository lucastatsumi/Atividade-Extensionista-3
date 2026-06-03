from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import User


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to restrict access to admin users only"""
    login_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == User.Role.ADMIN

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(self.login_url)
        return HttpResponseForbidden('Você não tem permissão para acessar esta página.')


class CoordenadorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to restrict access to coordinator users and above"""
    login_url = reverse_lazy('login')

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        return self.request.user.role in [User.Role.ADMIN, User.Role.COORDENADOR]

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(self.login_url)
        return HttpResponseForbidden('Você não tem permissão para acessar esta página.')


class ProfessorRequiredMixin(LoginRequiredMixin):
    """Mixin to restrict access to authenticated users (teachers and above)"""
    login_url = reverse_lazy('login')
