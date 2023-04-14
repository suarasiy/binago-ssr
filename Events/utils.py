from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List

from .models import Events, EventsUserRegistered
from django.shortcuts import get_object_or_404
from django.db.models import Q


def list_no_whitespace(n) -> List:
    return [x.strip() for x in n if x.strip()]


# def check_eligibility_register(request, slug: str) -> bool:
#     event: Events = get_object_or_404(request, slug=slug)
#     register_sheets: EventsUserRegistered = get_object_or_404(EventsUserRegistered, user=request.user, event=event)
#     return False if register_sheets.invoiceusereventregistered_set.filter(Q(status='WAITING') | Q(status='SUCCESS')).exists() else True
