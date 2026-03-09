from django import forms
from apps.eventos.models import Evento, Participante, Pagamento
from dal import autocomplete

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = '__all__'
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
        }

class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante
        exclude = ['valor_necessario', 'ativo']

class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = '__all__'
        widgets = {
            'data_pagamento': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'participante': autocomplete.ModelSelect2(
                url='eventos:participante-autocomplete',  # Namespace eventos
                forward=['evento']
            )
        }
