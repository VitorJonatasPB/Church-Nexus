from django.contrib import admin
from apps.eventos.models import Pagamento
from apps.eventos.forms import PagamentoForm

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    form = PagamentoForm
    list_display = ('participante_nome', 'valor_pago', 'forma_pagamento', 'confirmado', 'data_pagamento')
    search_fields = ('participante__nome', 'participante__email')
    list_filter = ('forma_pagamento', 'confirmado', 'conta')
    autocomplete_fields = ('participante', 'evento', 'conta')

    @admin.display(description="Participante")
    def participante_nome(self, obj):
        return obj.participante.nome if obj.participante else "Sem participante"

    class Media:
        js = ('eventos/admin_pagamento.js',)