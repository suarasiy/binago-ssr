from django.apps import AppConfig


class AssociationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Associations'

    def ready(self) -> None:
        from . import signals
