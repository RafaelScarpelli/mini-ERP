from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from django.urls import reverse_lazy


class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'

    def get_success_url(self):
        return reverse_lazy('dashboard')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'