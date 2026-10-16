from django.apps import AppConfig

class DjangoEventspipeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_eventspipe'
    verbose_name = 'Automations'

    def ready(self):
        import django_eventspipe.signals
