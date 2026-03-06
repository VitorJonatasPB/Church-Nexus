from django.contrib import admin
from apps.eventos.models import Participante

#@admin.register(Produto)
#class ProdutoAdmin(admin.ModelAdmin):
#    list_display = ('nome', 'preco', 'evento')
#    search_fields = ('nome', 'evento__nome')

@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'evento', 'total_pago_display', 'valor_necessario', 'pago')
    search_fields = ('nome', 'email', 'telefone')
    exclude = ('valor_necessario','ativo')  # Esconde os campos do formulário de edição
    autocomplete_fields = ('evento',)

    def total_pago_display(self, obj):
        return f"R$ {obj.total_pago:.2f}"  # <--- sem parênteses
    total_pago_display.short_description = "Total Pago"

    def pago(self, obj):
        return obj.total_pago >= obj.valor_necessario
    pago.boolean = True
    pago.short_description = "Pago?"







