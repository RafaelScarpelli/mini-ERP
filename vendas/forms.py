from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from .models import Cliente, Produto, Venda, ItemVenda, Pagamento, Categoria


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf_cnpj', 'telefone', 'email', 'endereco']
        widgets = {
            'endereco': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nome', css_class='col-md-8'),
                Column('cpf_cnpj', css_class='col-md-4'),
            ),
            Row(
                Column('telefone', css_class='col-md-6'),
                Column('email', css_class='col-md-6'),
            ),
            Field('endereco'),
            Submit('submit', 'Salvar', css_class='btn-green mt-2'),
        )


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'categoria', 'descricao', 'preco_venda', 'custo', 'estoque_atual']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nome', css_class='col-md-8'),
                Column('categoria', css_class='col-md-4'),
            ),
            Field('descricao'),
            Row(
                Column('preco_venda', css_class='col-md-4'),
                Column('custo', css_class='col-md-4'),
                Column('estoque_atual', css_class='col-md-4'),
            ),
            Submit('submit', 'Salvar', css_class='btn-green mt-2'),
        )


class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['cliente', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('cliente', css_class='col-md-8'),
                Column('status', css_class='col-md-4'),
            ),
            Submit('submit', 'Salvar', css_class='btn-green mt-2'),
        )
