from django import forms
from dal import autocomplete
from apps.secretaria.models import Membro, Area, Congregacao
from dal import autocomplete

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['nome']

class CongregacaoForm(forms.ModelForm):
    class Meta:
        model = Congregacao
        fields = '__all__'

class MembroForm(forms.ModelForm):
    class Meta:
        model = Membro
        fields = '__all__'
        widgets = {
            'data_de_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'congregacao': autocomplete.ModelSelect2(
                url='secretaria:congregacao-autocomplete',  # Nome da URL do DAL com a namespace correta
                forward=['area']                            # envia o valor de área para filtrar
            )
        }
