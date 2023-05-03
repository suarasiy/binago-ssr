from django.apps import AppConfig


class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Events'

    def ready(self) -> None:
        from . import signals
        return super().ready()