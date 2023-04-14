from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
    from typing import Type, Literal

from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from functools import wraps

from .models import Events, EventsUserRegistered


def check_eligibility_register(request, slug: str) -> bool:
    event: Events = get_object_or_404(Events, slug=slug)
    try:
        register_sheets: EventsUserRegistered = EventsUserRegistered.objects.get(user=request.user, event=event)
        return False if register_sheets.invoiceusereventregistered_set.filter(Q(status='WAITING') | Q(status='SUCCESS')).exists() else True
    except EventsUserRegistered.DoesNotExist:
        return True


def permission_check_eligibility_register(view):
    @wraps(view)
    def _view(request, *args, **kwargs) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
        # if request.method == "POST":
        if not check_eligibility_register(request, kwargs.get('slug', '')):
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return _view
