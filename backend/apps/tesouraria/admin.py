from django.contrib import admin
from .models import Conta, Categoria, Movimento


from django.urls import path
from apps.tesouraria.exports import (
    exportar_movimentos_csv, exportar_movimentos_pdf,
    exportar_extrato_conta_csv, exportar_extrato_conta_pdf
)

@admin.register(Conta)
class ContaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'saldo', 'ativa', 'criada_em')
    list_filter = ('ativa',)
    search_fields = ('nome',)
    change_form_template = "admin/tesouraria/conta/change_form.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/export/pdf/', self.admin_site.admin_view(self.export_pdf_view), name='tesouraria_conta_export_pdf'),
            path('<path:object_id>/export/excel/', self.admin_site.admin_view(self.export_excel_view), name='tesouraria_conta_export_excel'),
        ]
        return custom_urls + urls

    def export_pdf_view(self, request, object_id):
        conta = self.get_object(request, object_id)
        if not conta:
            from django.http import Http404
            raise Http404("Conta não encontrada")
        return exportar_extrato_conta_pdf(conta)
        
    def export_excel_view(self, request, object_id):
        conta = self.get_object(request, object_id)
        if not conta:
            from django.http import Http404
            raise Http404("Conta não encontrada")
        return exportar_extrato_conta_csv(conta)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo')
    list_filter = ('tipo',)
    search_fields = ('nome',)


@admin.register(Movimento)
class MovimentoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'valor', 'data', 'conta', 'categoria', 'membro', 'evento')
    list_filter = ('tipo', 'data', 'categoria', 'conta')
    search_fields = ('descricao',)
    autocomplete_fields = ('membro', 'evento')
    date_hierarchy = 'data'
    actions = [exportar_movimentos_csv, exportar_movimentos_pdf]
