from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from .models import Cliente, Produto, Venda, Categoria, ItemVenda
from .forms import ClienteForm, ProdutoForm, VendaForm, CategoriaForm


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


# ===== CATEGORIAS =====

class CategoriaListView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'vendas/categoria_list.html'
    context_object_name = 'categorias'
    ordering = ['nome']

    def get_queryset(self):
        return super().get_queryset().annotate(total_produtos=Count('produtos'))


class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'vendas/categoria_form.html'
    success_url = reverse_lazy('vendas:categoria-list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Nova Categoria'
        return ctx


class CategoriaUpdateView(LoginRequiredMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'vendas/categoria_form.html'
    success_url = reverse_lazy('vendas:categoria-list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Editar Categoria'
        return ctx


class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'vendas/confirm_delete.html'
    success_url = reverse_lazy('vendas:categoria-list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Excluir Categoria'
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

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Nova Venda'
        ctx['produtos'] = Produto.objects.filter(estoque_atual__gt=0).select_related('categoria').order_by('nome')
        return ctx

    def form_valid(self, form):
        produto_ids = self.request.POST.getlist('produto_id')
        quantidades = self.request.POST.getlist('quantidade')

        # Valida que pelo menos um item foi adicionado
        itens = []
        for pid, qty in zip(produto_ids, quantidades):
            try:
                qty = int(qty)
                if qty > 0:
                    itens.append((int(pid), qty))
            except (ValueError, TypeError):
                continue

        if not itens:
            form.add_error(None, 'Adicione pelo menos um produto à venda.')
            return self.form_invalid(form)

        try:
            with transaction.atomic():
                venda = form.save(commit=False)
                venda.usuario = self.request.user
                venda.save()

                total = 0
                for pid, qty in itens:
                    produto = get_object_or_404(Produto, pk=pid)

                    if qty > produto.estoque_atual:
                        raise ValueError(
                            f'Estoque insuficiente para "{produto.nome}". '
                            f'Disponível: {produto.estoque_atual}'
                        )

                    subtotal = produto.preco_venda * qty
                    ItemVenda.objects.create(
                        venda=venda,
                        produto=produto,
                        quantidade=qty,
                        preco_unitario=produto.preco_venda,
                        subtotal=subtotal,
                    )
                    produto.estoque_atual -= qty
                    produto.save()
                    total += subtotal

                venda.valor_total = total
                venda.save()

        except ValueError as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)

        messages.success(self.request, f'Venda #{venda.pk} registrada com sucesso!')
        return redirect(reverse_lazy('vendas:venda-detail', kwargs={'pk': venda.pk}))


class VendaDetailView(LoginRequiredMixin, DetailView):
    model = Venda
    template_name = 'vendas/venda_detail.html'
    context_object_name = 'venda'

    def get_queryset(self):
        return super().get_queryset().select_related('cliente', 'usuario').prefetch_related('itens__produto')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = f'Venda #{self.object.pk}'
        return ctx


class VendaCancelarView(LoginRequiredMixin, View):
    """Cancela uma venda e devolve o estoque dos produtos."""

    def post(self, request, pk):
        venda = get_object_or_404(Venda, pk=pk)

        if venda.status == 'CANCELADA':
            messages.error(request, 'Esta venda já está cancelada.')
            return redirect('vendas:venda-detail', pk=pk)

        if venda.status == 'FINALIZADA':
            messages.error(request, 'Vendas finalizadas não podem ser canceladas.')
            return redirect('vendas:venda-detail', pk=pk)

        with transaction.atomic():
            for item in venda.itens.select_related('produto').all():
                item.produto.estoque_atual += item.quantidade
                item.produto.save()

            venda.status = 'CANCELADA'
            venda.save()

        messages.success(request, f'Venda #{venda.pk} cancelada. Estoque revertido.')
        return redirect('vendas:venda-detail', pk=pk)


class ProdutoPrecoView(LoginRequiredMixin, View):
    """Retorna preço e estoque de um produto via AJAX."""

    def get(self, request, pk):
        produto = get_object_or_404(Produto, pk=pk)
        return JsonResponse({
            'preco': str(produto.preco_venda),
            'estoque': produto.estoque_atual,
            'nome': produto.nome,
        })