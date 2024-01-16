from django.apps import AppConfig


class BlankConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ganhos'

    def ready(self):
        import ganhos.signals
