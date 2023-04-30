from typing import Union, List, TYPE_CHECKING

if TYPE_CHECKING:
    from django.core.paginator import Page
    from django.db.models import QuerySet
    from binago.context_interface import Context as _
    from .models import Events
    from .forms import EventForm
    from django.forms import Form

    class IndexContext(_):
        events: Union[QuerySet, List[Events]]

    class IndexEventResourceContext(_):
        event: Events

    class IndexRegisteredEventsContext(_):
        registered_events: Page

    class FormContext(_):
        forms: EventForm
        forms_coverage: Form
        slug: str
