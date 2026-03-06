from django import forms
from .models import Conta, Categoria, Movimento

class ContaForm(forms.ModelForm):
    class Meta:
        model = Conta
        fields = ['nome','saldo', 'descricao', 'ativa']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'tipo']

class MovimentoForm(forms.ModelForm):
    class Meta:
        model = Movimento
        fields = ['tipo', 'valor', 'data', 'descricao', 'conta', 'categoria', 'membro', 'nome_participante', 'evento', 'comprovante']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }
