from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict, Literal
    from datetime import datetime

    CustomEventCollectionRender = TypedDict(
        '_', {
            'title': str,
            'start': str,
            'end': str,
            'customRender': bool,
            'colorStyle': Literal['calendar-red', 'calendar-blue', 'calendar-green'],
        }
    )

from .utils import pages_testing, pages_backend, pages_frontend, pages_handler

from django.contrib import messages

from django.urls import reverse
from django.utils import dateformat, timezone
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

from authentication.models import User
from Associations.query import user_registered_associations

from Events.permissions import check_eligibility_register, check_eligibility_user_register, check_eligibility_schedule_register, permission_check_user_eligibility, permission_check_schedule_eligibility
from Events.models import Events, EventsUserRegistered
from Invoices.models import InvoiceUserEventRegistered

import json
import pytz

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
    from .context import (
        SettingsContext, HomepageContext, EventDetailContext
    )


def get_calendar_color(start: datetime, end: datetime) -> Literal['calendar-red', 'calendar-blue', 'calendar-green']:
    now: datetime = timezone.localtime(datetime.today().replace(tzinfo=pytz.UTC))
    start = timezone.localtime(start)
    end = timezone.localtime(end)
    if end.date() < now.date():
        return 'calendar-red'
    if start.date() == now.date() or end.date() == now.date():
        return 'calendar-blue'
    return 'calendar-green'


def index(request) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    return redirect(reverse('homepage-event-upcoming'))


@require_http_methods(['GET'])
def homepage(request) -> HttpResponse:
    template: str = pages_frontend('homepage/index.html')
    now: datetime = timezone.localtime(timezone.now())
    events: QuerySet[Events] = Events.objects.filter(schedule_start__gte=now).order_by('-schedule_start')
    if request.user.is_authenticated:
        for event in events:
            event.user_eligibility = check_eligibility_user_register(request, event.slug)
            event.schedule_eligibility = check_eligibility_schedule_register(request, event.slug)
    else:
        for event in events:
            event.user_eligibility = check_eligibility_user_register(request, event.slug)
            event.schedule_eligibility = check_eligibility_schedule_register(request, event.slug)

    _: list = ['Business', 'Illustration', 'UI/UX Design', 'Web Development', 'Data Science', 'Big Data', 'Frontend Development', 'Backend Development',
               'Network Security', 'Developer Operations', 'Origami', 'Handcraft', 'Language', 'Rest API']

    context: HomepageContext = {
        'title': 'Binago homepage',
        'description': 'Explore the events.',
        'events': events,
        'categories': _
    }
    return render(request, template, context)


@require_http_methods(['GET'])
def homepage_past(request) -> HttpResponse:
    template: str = pages_frontend('homepage/index_past.html')
    now: datetime = timezone.localtime(timezone.now())
    events: QuerySet[Events] = Events.objects.filter(schedule_start__lte=now).order_by('-schedule_start')
    for event in events:
        event.user_eligibility = check_eligibility_user_register(request, event.slug)
        event.schedule_eligibility = False

    _: list = ['Business', 'Illustration', 'UI/UX Design', 'Web Development', 'Data Science', 'Big Data', 'Frontend Development', 'Backend Development',
               'Network Security', 'Developer Operations', 'Origami', 'Handcraft', 'Language', 'Rest API']

    context: HomepageContext = {
        'title': 'Binago Past Events',
        'description': 'Explore events archive.',
        'events': events,
        'categories': _
    }
    return render(request, template, context)


@require_http_methods(['GET'])
def timeline(request) -> HttpResponse:
    template: str = pages_frontend('homepage/all_timeline.html')
    now_month: int = timezone.localtime(timezone.now()).month
    events: QuerySet[Events] = Events.objects.filter(schedule_start__month=now_month)
    timelines: list[CustomEventCollectionRender] = []

    for event in events:
        timelines.append({
            'title': event.title,
            'start': str(event.schedule_start),
            'end': str(event.schedule_end),
            'customRender': True,
            'colorStyle': get_calendar_color(event.schedule_start, event.schedule_end)
        })

    context = {
        'timeline': json.dumps(timelines),
        'today': timezone.localtime(timezone.now())
    }
    return render(request, template, context)


@require_http_methods(['GET'])
def event_detail(request, slug) -> HttpResponse:
    template: str = pages_frontend('homepage/event_detail.html')
    register_eligibility: bool = check_eligibility_register(request, slug)
    context: EventDetailContext = {
        'title': 'Binago Events Detail',
        'description': 'Detail the events.',
        'event': get_object_or_404(Events, slug=slug),
        'register_eligibility': register_eligibility
    }
    return render(request, template, context)


@require_http_methods(['GET', 'POST'])
@permission_check_user_eligibility
@permission_check_schedule_eligibility
def event_register(request, slug) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
    event: Events = get_object_or_404(Events, slug=slug)
    # TODO: need to enhance this later
    register_eligibility: bool = check_eligibility_register(request, slug)
    if request.method == "POST":
        register_event: EventsUserRegistered
        _: bool
        register_event, _ = EventsUserRegistered.objects.get_or_create(
            event=event,
            user=request.user,
        )
        InvoiceUserEventRegistered.objects.create(
            event_registered=register_event,
            price=event.price,
            discount=0,
            status='SUCCESS'
        )
        schedule_start: str = dateformat.format(event.schedule_start, 'M d, Y h:i A')
        messages.success(
            request, f'Congratulations! You\'re registered to the event {event.title}. Please attend through follows the schedule {schedule_start}. For more information you can check dashboard page.')
        return redirect(reverse('homepage-event-detail', kwargs={'slug': slug}))
    else:
        pass
    template: str = pages_frontend('homepage/event_register.html')
    context: EventDetailContext = {
        'title': 'Binago Events Register',
        'description': 'Register the events.',
        'event': event,
        'register_eligibility': register_eligibility
    }
    return render(request, template, context)


@login_required
def dashboard(request) -> HttpResponse:
    template_name: str = pages_testing("dashboard.html")
    context = {
        'title': 'testing',
        'user': request.user
    }
    return render(request, template_name, context)


@login_required
@require_http_methods(['GET'])
def settings_profile(request) -> HttpResponse:
    template: str = pages_backend('settings/profile.html')
    user: User = User.objects.get(id=request.user.id)
    context: SettingsContext = {
        'title': 'Settings',
        'breadcrumb': {
            'main': 'Settings',
            'branch': [
                {
                    'name': 'Profile',
                    'reverse': reverse('settings'),
                    'type': 'current'
                }
            ]
        },
        'description': 'Maintain your profile appearance.',
        'powerheader': user,
        'registered_associations': user_registered_associations(request)
    }
    return render(request, template, context)


@require_http_methods(['GET'])
def signin(request) -> HttpResponse:
    template: str = pages_frontend('authentication/login.html')
    context: dict = {}
    return render(request, template, context)


@login_required
@require_http_methods(['POST'])
def signout(request) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    logout(request)
    return redirect('login')  # TODO: change it later


# TODO: change before production
def handle_403(request):
    template = 'handler/403.html'
    context = {}
    return render(request, template, context)


# TODO: change before production
def handle_404(request):
    template = 'handler/404.html'
    context = {}
    return render(request, template, context)


# TODO: change before production
def handle_500(request):
    template = 'handler/500.html'
    context = {}
    return render(request, template, context)
