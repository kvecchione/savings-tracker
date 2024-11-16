from django.apps import AppConfig

class Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "savings_tracker"

    def ready(self):
        import savings_tracker.signals
