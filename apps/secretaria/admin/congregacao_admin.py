from django.contrib import admin
from apps.secretaria.models import Congregacao

@admin.register(Congregacao)
class CongregacaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'area')
    search_fields = ('nome',)
    