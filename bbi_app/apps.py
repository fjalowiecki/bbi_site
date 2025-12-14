from django.apps import AppConfig

class BbiAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bbi_app'

    def ready(self):
        import bbi_app.signals