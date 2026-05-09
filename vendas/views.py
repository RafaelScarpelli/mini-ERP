from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Cliente, Produto, Venda
from .forms import ClienteForm, ProdutoForm, VendaForm


# ===== CLIENTES =====

class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'vendas/cliente_list.html'
    context_object_name = 'clientes'
    ordering = ['nome']


class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'vendas/cliente_form.html'
    success_url = reverse_lazy('vendas:cliente-list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Novo Cliente'
        return ctx


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'vendas/cliente_form.html'
    success_url = reverse_lazy('vendas:cliente-list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Editar Cliente'
        return ctx


class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'vendas/confirm_delete.html'
    success_url = reverse_lazy('vendas:cliente-list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Excluir Cliente'
        return ctx


# ===== PRODUTOS =====

class ProdutoListView(LoginRequiredMixin, ListView):
    model = Produto
    template_name = 'vendas/produto_list.html'
    context_object_name = 'produtos'
    ordering = ['nome']

    def get_queryset(self):
        return super().get_queryset().select_related('categoria')


class ProdutoCreateView(LoginRequiredMixin, CreateView):
    model = Produto
    form_class = ProdutoForm
    template_name = 'vendas/produto_form.html'
    success_url = reverse_lazy('vendas:produto-list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Novo Produto'
        return ctx


class ProdutoUpdateView(LoginRequiredMixin, UpdateView):
    model = Produto
    form_class = ProdutoForm
    template_name = 'vendas/produto_form.html'
    success_url = reverse_lazy('vendas:produto-list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Editar Produto'
        return ctx


class ProdutoDeleteView(LoginRequiredMixin, DeleteView):
    model = Produto
    template_name = 'vendas/confirm_delete.html'
    success_url = reverse_lazy('vendas:produto-list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Excluir Produto'
        return ctx


# ===== VENDAS =====

class VendaListView(LoginRequiredMixin, ListView):
    model = Venda
    template_name = 'vendas/venda_list.html'
    context_object_name = 'vendas'
    ordering = ['-data']

    def get_queryset(self):
        return super().get_queryset().select_related('cliente', 'usuario')


class VendaCreateView(LoginRequiredMixin, CreateView):
    model = Venda
    form_class = VendaForm
    template_name = 'vendas/venda_form.html'
    success_url = reverse_lazy('vendas:venda-list')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Nova Venda'
        return ctx