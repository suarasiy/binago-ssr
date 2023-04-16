from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, TypedDict, Union, Literal
    from django.db.models import QuerySet
    from authentication.models import User
    from Events.models import Events, EventsCategories
    from .context_interface import Context, ContextHomepage

    class NavigatePaginator(TypedDict):
        has_next: int
        has_previous: int

    class FilterCategories(TypedDict):
        reverse: str | Literal[False]
        data: QuerySet[EventsCategories]

    class HomepageContext(ContextHomepage, NavigatePaginator):
        # events: QuerySet[Events]
        events: Any
        categories: QuerySet[EventsCategories]
        type: Literal['UPCOMING', 'TODAY', 'PAST']

    class EventDetailContext(ContextHomepage):
        event: Events
        register_eligibility: bool

    class SettingsContext(Context):
        powerheader: User
