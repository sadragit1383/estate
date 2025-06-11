from django.apps import AppConfig


class EstateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.estate'



    def ready(self):
        import apps.estate.signal.signal