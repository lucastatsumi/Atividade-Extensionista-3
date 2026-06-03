from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import User


class LoginView(DjangoLoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.success(self.request, f'Bem-vindo, {form.cleaned_data.get("username")}!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Usuário ou senha incorretos.')
        return super().form_invalid(form)


class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Você foi desconectado com sucesso.')
        return super().dispatch(request, *args, **kwargs)

