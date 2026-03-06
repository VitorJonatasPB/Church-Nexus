from django.contrib import admin
from apps.secretaria.models import Membro
from apps.secretaria.forms import MembroForm

from apps.secretaria.exports import (
    exportar_membros_csv, exportar_membros_pdf,
    exportar_quantitativo_csv, exportar_quantitativo_pdf
)

@admin.register(Membro)
class MembroAdmin(admin.ModelAdmin):
    form = MembroForm
    list_display = ('foto_preview', 'nome', 'cargo', 'congregacao', 'area', 'ativo')
    list_filter = ('ativo', 'area', 'congregacao', 'cargo')
    readonly_fields = ("foto_preview",)
    search_fields = ('nome',)
    ordering = ('nome',)
    actions = [exportar_membros_csv, exportar_membros_pdf]

class QuantitativoMembro(Membro):
    class Meta:
        proxy = True
        verbose_name = "Quantitativo de Membros"
        verbose_name_plural = "Quantitativos de Membros"

@admin.register(QuantitativoMembro)
class QuantitativoMembroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cargo', 'congregacao', 'area', 'ativo')
    list_filter = ('area', 'congregacao')
    search_fields = ('nome',)
    actions = [exportar_quantitativo_csv, exportar_quantitativo_pdf]
    
    def has_add_permission(self, request):
        return False