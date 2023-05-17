from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Literal, TypedDict, Any
    from datetime import datetime
    from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
    from django.db.models import QuerySet
    from .context import Context

    CustomEventCollectionRender = TypedDict(
        '_', {
            'title': str,
            'start': str,
            'end': str,
            'customRender': bool,
            'colorStyle': Literal['calendar-red', 'calendar-blue', 'calendar-green'],
        }
    )

import calendar
from django.db.models import F, Q, Count
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from binago.utils import pages_backend, timezone_now as now

from Events.models import Events
from Associations.query import user_registered_associations
from authentication.permissions import permission_staff_only

from datetime import datetime
import pytz
import json


def get_calendar_color(start: datetime, end: datetime) -> Literal['calendar-red', 'calendar-blue', 'calendar-green']:
    now: datetime = timezone.localtime(datetime.today().replace(tzinfo=pytz.UTC))
    start = timezone.localtime(start)
    end = timezone.localtime(end)
    if end.date() < now.date():
        return 'calendar-red'
    if start.date() == now.date() or end.date() == now.date():
        return 'calendar-blue'
    return 'calendar-green'


@login_required
@require_http_methods(['GET'])
@permission_staff_only
def events(request) -> HttpResponse:
    # monthly (default: now().month)
    summary_by_categories = Events.objects.values(
        name=F("category__category")).annotate(value=Count('category')) \
        .filter(schedule_start__month=now().month, schedule_start__year=now().year, schedule_end__month=now().month, schedule_end__year=now().year, is_published=True)

    number_of_days_in_month = list(range(1, calendar.monthrange(now().year, now().month)[1]+1))

    events: QuerySet[Events] = Events.objects.filter(
        schedule_start__month=now().month, schedule_start__year=now().year,
        schedule_end__month=now().month, schedule_end__year=now().year, is_published=True)

    events_collection: list[CustomEventCollectionRender] = []

    # summary for `total registered users into events` monthly
    aggregate_summary_user_registered = Events.objects.values(day=F('eventsuserregistered__updated_at__day')).annotate(
        value=Count('eventsuserregistered', filter=Q(
            eventsuserregistered__invoiceusereventregistered__status="SUCCESS")),
    ).filter(schedule_start__month=now().month, schedule_start__year=now().year, schedule_end__month=now().month, schedule_end__year=now().year, is_published=True, eventsuserregistered__invoiceusereventregistered__status="SUCCESS")
    summary_user_registered = {'x_label': number_of_days_in_month}

    tmp_of_summary_registered_users = []
    for x in range(1, len(number_of_days_in_month)+1):
        tmp_of_summary_registered_users.append(0)
        for _, obj in enumerate(aggregate_summary_user_registered):
            if x == obj.get('day', False):
                tmp_of_summary_registered_users[x-1] = obj.get('value', 0)

    summary_user_registered.update({'data': tmp_of_summary_registered_users})
    # end of summary for `total registered users into events` monthly



    # summary for `total registered events` monthly (published and not published)
    aggregate_summary_events_registered_published = Events.objects.values(day=F('created_at__day')).annotate(value=Count('id')).filter(is_published=True, created_at__month=now().month, created_at__year=now().year)
    aggregate_summary_events_registered_unpublished = Events.objects.values(day=F('created_at__day')).annotate(value=Count('id')).filter(is_published=False, created_at__month=now().month, created_at__year=now().year)
    summary_events_registered = { 'x_label': number_of_days_in_month }

    coord_events_registered = {
        'published': [],
        'unpublished': []
    }
    for x in range(1, len(number_of_days_in_month)+1):
        coord_events_registered['published'].append(0)
        coord_events_registered['unpublished'].append(0)
        for _, obj in enumerate(aggregate_summary_events_registered_published):
            if x == obj.get('day', False):
                coord_events_registered['published'][x-1] = obj.get('value', 0)
        for _, obj in enumerate(aggregate_summary_events_registered_unpublished):
            if x == obj.get('day', False):
                coord_events_registered['unpublished'][x-1] = obj.get('value', 0)

    summary_events_registered.update({
        'data_published': coord_events_registered['published'],
        'data_unpublished': coord_events_registered['unpublished']
    })

    # end of summary for `total registered events`
    
    
    
    # summary accumulation yearly
    
    month: list[int]
    months_abbr, month = calendar.month_abbr[1:], list(range(1, 13))
    summary_accumulation_yearly: Any = { 'y_label': months_abbr }
    aggregate_yearly_events_unpublished = Events.objects.values(month=F('created_at__month')).annotate(value=Count('id')).filter(is_published=False, created_at__year=now().year)
    aggregate_yearly_events_published = Events.objects.values(month=F('created_at__month')).annotate(value=Count('id')).filter(is_published=True, created_at__year=now().year)
    aggregate_yearly_users_registered = Events.objects.values(month=F('eventsuserregistered__updated_at__month')).annotate(
        value=Count('eventsuserregistered', filter=Q(
            eventsuserregistered__invoiceusereventregistered__status="SUCCESS")),
    ).filter(schedule_start__year=now().year,schedule_end__year=now().year, is_published=True, eventsuserregistered__invoiceusereventregistered__status="SUCCESS")

    coord_accumulation_yearly = {
        'events_published': [],
        'events_unpublished': [],
        'users_registered': []
    }

    for x in month:
        coord_accumulation_yearly['events_published'].append(0)
        coord_accumulation_yearly['events_unpublished'].append(0)
        coord_accumulation_yearly['users_registered'].append(0)
        for _, obj in enumerate(aggregate_yearly_events_published):
            if x == obj.get('month', False):
                coord_accumulation_yearly['events_published'][x-1] = obj.get('value', 0)
        for _, obj in enumerate(aggregate_yearly_events_unpublished):
            if x == obj.get('month', False):
                coord_accumulation_yearly['events_unpublished'][x-1] = obj.get('value', 0)
        for _, obj in enumerate(aggregate_yearly_users_registered):
            if x == obj.get('month', False):
                coord_accumulation_yearly['users_registered'][x-1] = obj.get('value', 0)

    summary_accumulation_yearly.update({
        'data': coord_accumulation_yearly
    })

    # end of accumulation yearly

    for event in events:
        event_start: datetime = timezone.localtime(event.schedule_start.replace(tzinfo=pytz.UTC))
        event_end: datetime = timezone.localtime(event.schedule_end.replace(tzinfo=pytz.UTC))

        events_collection.append({
            'title': event.title,
            'start': str(event.schedule_start),
            'end': str(event.schedule_end),
            'customRender': True,
            'colorStyle': get_calendar_color(event_start, event_end),
        })

    template: str = pages_backend('dashboard/events.html')
    context = {
        'title': 'Events',
        'breadcrumb': {
            'main': 'Overview',
            'branch': [
                {
                    'name': 'Events',
                    'reverse': reverse('dashboard-events'),
                    'type': 'current'
                },
            ]
        },
        'description': 'Here is the summaries about the recent events over the month.',
        'timeline': json.dumps(events_collection),
        'summary_by_categories': json.dumps(list(summary_by_categories)),
        'summary_user_registered': json.dumps(summary_user_registered),
        'summary_events_registered': json.dumps(summary_events_registered),
        'summary_accumulation_yearly': json.dumps(summary_accumulation_yearly),
        'header': request.user.avatar,
        'registered_associations': user_registered_associations(request)
    }
    return render(request, template, context)
