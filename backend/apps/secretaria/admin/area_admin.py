from django.contrib import admin
from apps.secretaria.models import Area

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('nome',)


