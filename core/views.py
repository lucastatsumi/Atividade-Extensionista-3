from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from accounts.models import User


class DashboardView(LoginRequiredMixin, TemplateView):
    """Main dashboard view"""
    template_name = 'core/dashboard.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard'
        return context

