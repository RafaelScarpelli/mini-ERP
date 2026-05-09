from django.urls import path
from . import views

app_name = 'vendas'

urlpatterns = [
    # Vendas
    path('', views.VendaListView.as_view(), name='venda-list'),
    path('nova/', views.VendaCreateView.as_view(), name='venda-create'),

    # Produtos
    path('produtos/', views.ProdutoListView.as_view(), name='produto-list'),
    path('produtos/novo/', views.ProdutoCreateView.as_view(), name='produto-create'),
    path('produtos/<int:pk>/editar/', views.ProdutoUpdateView.as_view(), name='produto-update'),
    path('produtos/<int:pk>/excluir/', views.ProdutoDeleteView.as_view(), name='produto-delete'),

    # Clientes
    path('clientes/', views.ClienteListView.as_view(), name='cliente-list'),
    path('clientes/novo/', views.ClienteCreateView.as_view(), name='cliente-create'),
    path('clientes/<int:pk>/editar/', views.ClienteUpdateView.as_view(), name='cliente-update'),
    path('clientes/<int:pk>/excluir/', views.ClienteDeleteView.as_view(), name='cliente-delete'),
]