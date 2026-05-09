from django.urls import path
from django.views.generic import TemplateView

app_name = 'vendas'

urlpatterns = [
    path('', TemplateView.as_view(template_name='base.html'), name='venda-list'),
    path('produtos/', TemplateView.as_view(template_name='base.html'), name='produto-list'),
    path('clientes/', TemplateView.as_view(template_name='base.html'), name='cliente-list'),
]