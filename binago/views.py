from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict, Literal
    from datetime import datetime
    from authentication.context import ProfileContext

    CustomEventCollectionRender = TypedDict(
        '_', {
            'title': str,
            'start': str,
            'end': str,
            'customRender': bool,
            'colorStyle': Literal['calendar-red', 'calendar-blue', 'calendar-green'],
            'url': str
        }
    )

from .utils import timezone_now, pages_testing, pages_backend, pages_frontend, pages_handler
from .query import fragment_info

from django.contrib import messages

from binago.utils import SNAP
from django.urls import reverse
from django.utils import dateformat, timezone
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

from authentication.models import User
from Associations.query import user_registered_associations
from Associations.models import AssociationsGroup

from Events.permissions import check_eligibility_register, check_eligibility_user_register, check_eligibility_schedule_register, check_eligibility_seat, permission_check_user_eligibility, permission_check_schedule_eligibility, permission_check_seat_eligibility, permission_check_event_is_published
from Events.models import Events, EventsUserRegistered, EventsCategories
from Invoices.models import InvoiceUserEventRegistered

import json
import pytz

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
    from .context import (
        SettingsContext, HomepageContext, EventDetailContext, EventRegisterContext
    )


def get_calendar_color(start: datetime, end: datetime) -> Literal['calendar-red', 'calendar-blue', 'calendar-green']:
    now: datetime = timezone.localtime(timezone.now().replace(tzinfo=pytz.UTC))
    start = timezone.localtime(start.replace(tzinfo=pytz.UTC))
    end = timezone.localtime(end.replace(tzinfo=pytz.UTC))
    if end.date() < now.date():
        return 'calendar-red'
    if start.date() == now.date() or end.date() == now.date():
        return 'calendar-blue'
    return 'calendar-green'


def index(request) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    return redirect(reverse('homepage-event-upcoming'))


def stub_homepage_events(request, events: QuerySet[Events], max_item_per_page: int, _type: Literal['UPCOMING', 'TODAY', 'PAST']) -> HomepageContext:
    page: int = int(request.GET.get('page', 1))
    now: datetime = timezone.localtime(timezone.now())
    published_only_events: QuerySet[Events] = events.filter(is_published=True)
    for event in published_only_events:
        event.user_eligibility = check_eligibility_user_register(request, event.slug)
        if timezone.localtime(event.schedule_end.replace(tzinfo=pytz.UTC)) < now:
            event.schedule_eligibility = False
        else:
            event.schedule_eligibility = check_eligibility_schedule_register(request, event.slug)
        event.seat_eligibility = check_eligibility_seat(request, event.slug)

    _: QuerySet[EventsCategories] = EventsCategories.objects.all().order_by('category')

    cluster_events = Paginator(published_only_events, max_item_per_page)
    return {
        'title': 'Binago Past Events',
        'description': 'Explore events archive.',
        'events': cluster_events.get_page(page),
        'categories': _,
        'has_next': page + 1 if cluster_events.get_page(page).has_next() else False,
        'has_previous': page - 1 if cluster_events.get_page(page).has_previous() else False,
        'type': _type,
        'fragment': fragment_info()
    }


@require_http_methods(['GET'])
def homepage(request, *args, **kwargs) -> HttpResponse:
    template: str = pages_frontend('homepage/index.html')
    now: datetime = timezone.localtime(timezone.now())
    category: str | Literal[False] = kwargs.get('category', False)
    if category:
        events: QuerySet[Events] = Events.objects.filter(
            schedule_start__gte=now, category__slug=category).order_by('-schedule_start')
    else:
        events: QuerySet[Events] = Events.objects.filter(schedule_start__gte=now).order_by('-schedule_start')

    context: HomepageContext = stub_homepage_events(request, events, 6, 'UPCOMING')
    context['title'] = 'Binago Homepage | Upcoming Events'
    context['description'] = 'Explore the upcoming events.'
    return render(request, template, context)


def homepage_category(request, category) -> HttpResponse:
    return homepage(request, category=category)


@require_http_methods(['GET'])
def homepage_past(request, *args, **kwargs) -> HttpResponse:
    template: str = pages_frontend('homepage/index.html')
    now: datetime = timezone_now()
    category: str | Literal[False] = kwargs.get('category', False)
    if category:
        events: QuerySet[Events] = Events.objects.filter(
            schedule_start__lte=now, category__slug=category).order_by('-schedule_start')
    else:
        events: QuerySet[Events] = Events.objects.filter(schedule_start__lte=now).order_by('-schedule_start')

    context: HomepageContext = stub_homepage_events(request, events, 6, 'PAST')
    context['title'] = 'Binago Homepage | Past Events'
    context['description'] = 'Explore the archived events.'
    return render(request, template, context)


def homepage_past_category(request, category) -> HttpResponse:
    return homepage_past(request, category=category)


@require_http_methods(['GET'])
def homepage_today(request, *args, **kwargs) -> HttpResponse:
    template: str = pages_frontend('homepage/index.html')
    category: str | Literal[False] = kwargs.get('category', False)
    if category:
        events: QuerySet[Events] = Events.objects.filter(
            schedule_start__month=timezone_now().month, schedule_start__day=timezone_now().day, category__slug=category).order_by('-schedule_start')
    else:
        events: QuerySet[Events] = Events.objects.filter(
            schedule_start__month=timezone_now().month, schedule_start__day=timezone_now().day).order_by('-schedule_start')

    context: HomepageContext = stub_homepage_events(request, events, 6, 'TODAY')
    context['title'] = 'Binago Homepage | Today Events'
    context['description'] = 'Explore today events.'
    return render(request, template, context)


def homepage_today_category(request, category) -> HttpResponse:
    return homepage_today(request, category=category)


@require_http_methods(['GET'])
def timeline(request) -> HttpResponse:
    template: str = pages_frontend('homepage/all_timeline.html')
    events: QuerySet[Events] = Events.objects.filter(
        schedule_start__month=timezone_now().month, schedule_start__year=timezone_now().year, is_published=True)
    timelines: list[CustomEventCollectionRender] = []

    for event in events:
        timelines.append({
            'title': event.title,
            'start': str(timezone.localtime(event.schedule_start.replace(tzinfo=pytz.UTC))),
            'end': str(timezone.localtime(event.schedule_end.replace(tzinfo=pytz.UTC))),
            'customRender': True,
            'colorStyle': get_calendar_color(event.schedule_start, event.schedule_end),
            'url': reverse('homepage-event-detail', kwargs={'slug': event.slug})
        })

    context = {
        'timeline': json.dumps(timelines),
        'today': timezone.localtime(timezone.now())
    }
    return render(request, template, context)


@require_http_methods(['GET'])
@permission_check_event_is_published
def event_detail(request, slug) -> HttpResponse:
    template: str = pages_frontend('homepage/event_detail.html')
    register_eligibility: bool = check_eligibility_register(request, slug)
    event: Events = get_object_or_404(Events, slug=slug)
    # TODO: typechecking need to fix
    event_associated = Events.objects.get(slug=slug).association_group.association  # type: ignore
    association_events: QuerySet[Events] = Events.objects.filter(
        association_group__association=event_associated, is_published=True).order_by('-schedule_start').exclude(id=event.id)
    count_registrant: QuerySet[EventsUserRegistered] = EventsUserRegistered.objects.filter(event=event)
    cluster_association_events = Paginator(association_events, 3)
    context: EventDetailContext = {
        'title': 'Binago Events Detail',
        'description': 'Detail the events.',
        'event': event,
        'register_eligibility': register_eligibility,
        'association_events': cluster_association_events.get_page(1),
        'event_ended': True if event.schedule_end < timezone_now() else False,
        'fragment': fragment_info(),
        'total_registrant': count_registrant.count()
    }
    return render(request, template, context)


@login_required
@require_http_methods(['GET', 'POST'])
@permission_check_event_is_published
@permission_check_user_eligibility
@permission_check_schedule_eligibility
@permission_check_seat_eligibility
def event_register(request, slug) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
    snap = SNAP()
    event: Events = get_object_or_404(Events, slug=slug)
    # TODO: need to enhance this later
    register_eligibility: bool = check_eligibility_register(request, slug)
    user: User = get_object_or_404(User, id=request.user.id)
    if request.method == "POST":
        register_event: EventsUserRegistered
        _: bool
        register_event, _ = EventsUserRegistered.objects.get_or_create(
            event=event,
            user=request.user,
        )
        invoice: InvoiceUserEventRegistered = InvoiceUserEventRegistered.objects.create(
            event_registered=register_event,
            price=event.price,
            discount=0,
        )
        if event.price == 0:
            invoice.status = 'SUCCESS'
            invoice.save()
        else:
            param = {
                "transaction_details": {
                    "order_id": str(invoice.uuid),
                    "gross_amount": invoice.price
                }, "credit_card": {
                    "secure": True
                }, "customer_details": {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "phone": "",
                    "city": user.city,
                }
            }
            transaction_capture = snap.init_new().create_transaction(param)
            print("=== TRANSACTION CAPTURE ===")
            print(transaction_capture.get('token', False))
            print("=== END CAPTURE ===")

            # update midtrans token to the db
            invoice.midtrans_token = transaction_capture.get('token', None)
            invoice.save()

        schedule_start: str = dateformat.format(event.schedule_start, 'M d, Y h:i A')
        messages.success(
            request, f'Congratulations! You\'re registered to the event {event.title}. Please attend through follows the schedule {schedule_start}. For more information you can check dashboard page.')
        return redirect(reverse('homepage-event-detail', kwargs={'slug': slug}))
    else:
        pass
    template: str = pages_frontend('homepage/event_register.html')
    context: EventRegisterContext = {
        'title': 'Binago Events Register',
        'description': 'Register the events.',
        'event': event,
        'register_eligibility': register_eligibility,
        'fragment': fragment_info()
    }
    return render(request, template, context)


def index_certificate(request, uuid) -> HttpResponse:
    # TODO: improve
    template: str = pages_frontend('certificate/index.html')
    context = {
        'title': 'test'
    }
    return render(request, template, context)


@login_required
def dashboard(request) -> HttpResponse:
    # TODO: improve
    template: str = pages_testing("dashboard.html")
    context = {
        'title': 'testing',
        'user': request.user
    }
    return render(request, template, context)


@login_required
@require_http_methods(['GET'])
def settings_profile(request) -> HttpResponse:
    template: str = pages_backend('settings/profile.html')
    user: User = User.objects.get(id=request.user.id)
    group: QuerySet[AssociationsGroup] = AssociationsGroup.objects.filter(
        user=user, association__approval__is_approved=True)
    context: ProfileContext = {
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
        'group': group,
        'registered_associations': user_registered_associations(request),
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
    return redirect(reverse('homepage'))


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
