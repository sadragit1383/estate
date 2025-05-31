from django.apps import AppConfig


class AgencyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.agency'


    def ready(self):
        import apps.agency.signal.agency_signal