from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, TypedDict, Union, Literal
    from django.core.paginator import Page
    from django.db.models import QuerySet
    from authentication.models import User
    from Events.models import Events, EventsCategories
    from .context_interface import Context, ContextHomepage
    from midtransclient import Snap

    class NavigatePaginator(TypedDict):
        has_next: int
        has_previous: int

    class FilterCategories(TypedDict):
        reverse: str | Literal[False]
        data: QuerySet[EventsCategories]

    class HomepageContext(ContextHomepage, NavigatePaginator):
        # events: QuerySet[Events]
        events: Page
        categories: QuerySet[EventsCategories]
        type: Literal['UPCOMING', 'TODAY', 'PAST', 'ON_AIR']

    class EventDetailContext(ContextHomepage):
        event: Events
        register_eligibility: bool
        association_events: Page
        event_ended: bool
        total_registrant: int

    class EventRegisterContext(ContextHomepage):
        event: Events
        register_eligibility: bool

    class SettingsContext(Context):
        powerheader: User

    class QueryFragmentInfoContext(TypedDict):
        registered_users: int
        registered_associations: int
        registered_events: int

    class UtilSnapContext(TypedDict):
        snap: Snap
        SERVER_KEY: str
        CLIENT_KEY: str
