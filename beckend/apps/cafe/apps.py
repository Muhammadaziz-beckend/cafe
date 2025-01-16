from django.apps import AppConfig


class CafeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.cafe"

    def ready(self):
        import apps.cafe.signals
