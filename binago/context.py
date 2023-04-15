from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from authentication.models import User
    from Events.models import Events
    from .context_interface import Context, ContextHomepage

    class HomepageContext(ContextHomepage):
        events: QuerySet[Events]
        categories: list

    class EventDetailContext(ContextHomepage):
        event: Events
        register_eligibility: bool

    class SettingsContext(Context):
        powerheader: User
