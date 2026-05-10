from django.urls import path
from . import views

app_name = 'vendas'

urlpatterns = [
    # Vendas
    path('', views.VendaListView.as_view(), name='venda-list'),
    path('nova/', views.VendaCreateView.as_view(), name='venda-create'),
    path('<int:pk>/', views.VendaDetailView.as_view(), name='venda-detail'),
    path('<int:pk>/cancelar/', views.VendaCancelarView.as_view(), name='venda-cancelar'),

    # API interna: preço de produto (AJAX)
    path('api/produto/<int:pk>/preco/', views.ProdutoPrecoView.as_view(), name='produto-preco'),

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

    # Categorias
    path('categorias/', views.CategoriaListView.as_view(), name='categoria-list'),
    path('categorias/nova/', views.CategoriaCreateView.as_view(), name='categoria-create'),
    path('categorias/<int:pk>/editar/', views.CategoriaUpdateView.as_view(), name='categoria-update'),
    path('categorias/<int:pk>/excluir/', views.CategoriaDeleteView.as_view(), name='categoria-delete'),
]