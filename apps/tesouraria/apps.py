from django.apps import AppConfig

class TesourariaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.tesouraria'

    def ready(self):
        import apps.tesouraria.signals
