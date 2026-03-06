from django.contrib import admin
from apps.eventos.models import Evento, Participante, Pagamento
from django.utils.html import format_html
from django.db.models import Sum, F
from django.urls import path
from apps.eventos.exports import exportar_evento_csv, exportar_evento_pdf, exportar_eventos_csv, exportar_eventos_pdf


class ParticipanteInline(admin.TabularInline):
    model = Participante
    extra = 0
    can_delete = False
    fields = ('nome', 'telefone', 'email', 'total_pago_display', 'ativo', 'data_inscricao')
    readonly_fields = ('nome', 'telefone', 'email', 'total_pago_display', 'ativo', 'data_inscricao')
    show_change_link = True

    def total_pago_display(self, obj):
        if not obj:
            return "R$ 0.00"
        return f"R$ {obj.total_pago:.2f}"  # sem ()
    total_pago_display.short_description = "Total Pago"


    def ativo(self, obj):
        if not obj:
            return "-"
        return format_html('<span style="color:green;">✔️</span>' if obj.ativo else '<span style="color:red;">❌</span>')
    ativo.short_description = "Ativo"

class PagamentoInline(admin.TabularInline):
    model = Pagamento
    extra = 0
    fields = ('participante', 'valor_pago', 'forma_pagamento', 'confirmado', 'data_pagamento')
    readonly_fields = ('data_pagamento',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "participante":
            object_id = request.resolver_match.kwargs.get('object_id')
            if object_id:
                kwargs["queryset"] = Participante.objects.filter(evento_id=object_id)
            else:
                kwargs["queryset"] = Participante.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_inicio', 'data_fim', 'valor_necessario', 'total_arrecadado',)
    search_fields = ('nome',)
    list_filter = ('data_inicio', 'data_fim')
    inlines = [ParticipanteInline, PagamentoInline]
    actions = [exportar_eventos_csv, exportar_eventos_pdf]
    change_form_template = "admin/eventos/evento/change_form.html"
    
    def total_arrecadado(self, obj):
        total = Pagamento.objects.filter(
            participante__evento=obj
        ).aggregate(total=Sum('valor_pago'))['total'] or 0
        return f"R$ {total}"
    total_arrecadado.short_description = "Total Arrecadado"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/export/pdf/', self.admin_site.admin_view(self.export_pdf_view), name='eventos_evento_export_pdf'),
            path('<path:object_id>/export/excel/', self.admin_site.admin_view(self.export_excel_view), name='eventos_evento_export_excel'),
        ]
        return custom_urls + urls

    def export_pdf_view(self, request, object_id):
        evento = self.get_object(request, object_id)
        if not evento:
            from django.http import Http404
            raise Http404("Evento não encontrado")
        return exportar_evento_pdf(evento)
        
    def export_excel_view(self, request, object_id):
        evento = self.get_object(request, object_id)
        if not evento:
            from django.http import Http404
            raise Http404("Evento não encontrado")
        return exportar_evento_csv(evento)