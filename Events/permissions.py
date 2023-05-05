from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
    from typing import Type, Literal
    from datetime import datetime
    from django.db.models import QuerySet

import pytz

from django.db.models import Q
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from functools import wraps

from authentication.permissions import manager_bypass
from authentication.models import User
from Events.models import EventsUserRegistered
from .models import Events, EventsUserRegistered
from Invoices.models import InvoiceUserEventRegistered


def check_eligibility_schedule_register(request, slug: str) -> bool:
    event: Events = get_object_or_404(Events, slug=slug)
    end: datetime = event.schedule_end.replace(tzinfo=pytz.UTC)
    return False if timezone.localtime(timezone.now()) > timezone.localtime(end) else True


def check_eligibility_user_register(request, slug: str) -> bool:
    # TODO: may be better if refactor this
    if not request.user.is_authenticated:
        return True
    event: Events = get_object_or_404(Events, slug=slug)
    try:
        register_sheets: EventsUserRegistered = EventsUserRegistered.objects.get(user=request.user, event=event)
        return False if register_sheets.invoiceusereventregistered_set.filter(Q(status='WAITING') | Q(status='SUCCESS')).exists() else True
    except EventsUserRegistered.DoesNotExist:
        return True


def check_eligibility_seat(request, slug: str) -> bool:
    event: Events = get_object_or_404(Events, slug=slug)
    # TODO: need to fix later
    check_seat: QuerySet[EventsUserRegistered] = EventsUserRegistered.objects.filter(event=event)
    if check_seat.count() >= event.max_audience:
        return False
    return True


def check_eligibility_register(request, slug: str) -> bool:
    if not check_eligibility_user_register(request, slug):
        return False
    if not check_eligibility_schedule_register(request, slug):
        return False
    if not check_eligibility_seat(request, slug):
        return False
    return True


def check_event_creator_only(request, slug_event) -> bool:
    event: Events = get_object_or_404(Events, slug=slug_event)
    # TODO: [typehint] problem with None since event.association_group allowed to be null
    if not event.association_group.user == request.user:  # type: ignore
        return False
    return True


def permission_check_schedule_eligibility(view):
    @wraps(view)
    def _view(request, *args, **kwargs) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
        if not check_eligibility_schedule_register(request, kwargs.get('slug', '')):
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return _view


def permission_check_user_eligibility(view):
    @wraps(view)
    def _view(request, *args, **kwargs) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
        if not check_eligibility_user_register(request, kwargs.get('slug', '')):
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return _view


def permission_check_seat_eligibility(view):
    @wraps(view)
    def _view(request, *args, **kwargs) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
        if not check_eligibility_seat(request, kwargs.get('slug', '')):
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return _view


def permission_check_user_registered_into_event(view):
    @wraps(view)
    def _view(request, *args, **kwargs) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
        try:
            ticket: EventsUserRegistered = EventsUserRegistered.objects.get(id=kwargs.get('ticket_id', ''))
            if not InvoiceUserEventRegistered.objects.filter(event_registered=ticket, status='SUCCESS').exists():
                raise PermissionDenied
        except EventsUserRegistered.DoesNotExist:
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return _view


def permission_check_event_is_published(view):
    @wraps(view)
    def _view(request, *args, **kwargs) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
        event: Events = get_object_or_404(Events, slug=kwargs.get('slug', ''))
        if not event.is_published:
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return _view


def permission_check_event_creator_only(view):
    @wraps(view)
    def _view(request, *args, **kwargs) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect | PermissionDenied:
        if not check_event_creator_only(request, kwargs.get('slug_event', '')):
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return _view


def permission_check_event_creator_only_manager_bypass(view):
    @wraps(view)
    def _view(request, *args, **kwargs) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
        if manager_bypass(request):
            return view(request, *args, **kwargs)
        if not check_event_creator_only(request, kwargs.get('slug_event', '')):
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return _view
