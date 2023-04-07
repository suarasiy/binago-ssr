from typing import Union, List, TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from binago.context_interface import Context as _
    from .models import Events
    from .forms import EventForm

    class IndexContext(_):
        events: Union[QuerySet, List[Events]]

    class FormContext(_):
        forms: EventForm
        slug: str
