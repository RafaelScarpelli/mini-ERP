from django.db import models


# ================= ENUMS =================

class StatusVenda(models.TextChoices):
    ORCAMENTO  = 'ORCAMENTO',  'Orçamento'
    FINALIZADA = 'FINALIZADA', 'Finalizada'
    CANCELADA  = 'CANCELADA',  'Cancelada'


class TipoMovimentacao(models.TextChoices):
    ENTRADA = 'ENTRADA', 'Entrada'
    SAIDA   = 'SAIDA',   'Saída'


class FormaPagamento(models.TextChoices):
    DINHEIRO = 'DINHEIRO', 'Dinheiro'
    CARTAO   = 'CARTAO',   'Cartão'
    PIX      = 'PIX',      'Pix'
    BOLETO   = 'BOLETO',   'Boleto'


# ================= MODELS =================

class Cliente(models.Model):
    nome      = models.CharField(max_length=255)
    cpf_cnpj  = models.CharField(max_length=18, unique=True)
    telefone  = models.CharField(max_length=20, blank=True)
    email     = models.EmailField(blank=True)
    endereco  = models.TextField(blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'


class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'


class Produto(models.Model):
    categoria    = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='produtos')
    nome         = models.CharField(max_length=255)
    descricao    = models.TextField(blank=True)
    preco_venda  = models.DecimalField(max_digits=10, decimal_places=2)
    custo        = models.DecimalField(max_digits=10, decimal_places=2)
    estoque_atual = models.IntegerField(default=0)

    def baixar_estoque(self, qtd):
        if qtd > self.estoque_atual:
            raise ValueError('Estoque insuficiente.')
        self.estoque_atual -= qtd
        self.save()

    def adicionar_estoque(self, qtd):
        self.estoque_atual += qtd
        self.save()

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'


class Venda(models.Model):
    usuario     = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='vendas')
    cliente     = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, related_name='vendas')
    data        = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status      = models.CharField(max_length=20, choices=StatusVenda.choices, default=StatusVenda.ORCAMENTO)

    def calcular_total(self):
        self.valor_total = sum(item.subtotal for item in self.itens.all())
        self.save()

    def finalizar(self):
        self.status = StatusVenda.FINALIZADA
        self.save()

    def cancelar(self):
        self.status = StatusVenda.CANCELADA
        self.save()

    def __str__(self):
        return f'Venda #{self.pk} — {self.status}'

    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'


class ItemVenda(models.Model):
    venda          = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='itens')
    produto        = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name='itens_venda')
    quantidade     = models.IntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal       = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calcular_subtotal(self):
        self.subtotal = self.quantidade * self.preco_unitario
        self.save()

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome}'

    class Meta:
        verbose_name = 'Item de Venda'
        verbose_name_plural = 'Itens de Venda'


class Pagamento(models.Model):
    venda          = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='pagamentos')
    valor          = models.DecimalField(max_digits=10, decimal_places=2)
    data_pagamento = models.DateField()
    forma          = models.CharField(max_length=20, choices=FormaPagamento.choices)

    def __str__(self):
        return f'{self.forma} — R$ {self.valor}'

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'


class MovimentacaoEstoque(models.Model):
    produto    = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='movimentacoes')
    tipo       = models.CharField(max_length=10, choices=TipoMovimentacao.choices)
    quantidade = models.IntegerField()
    data       = models.DateTimeField(auto_now_add=True)
    origem     = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.tipo} — {self.quantidade}x {self.produto.nome}'

    class Meta:
        verbose_name = 'Movimentação de Estoque'
        verbose_name_plural = 'Movimentações de Estoque'