from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from authentication.models import User
    from .context_interface import Context

    class SettingsContext(Context):
        powerheader: User
