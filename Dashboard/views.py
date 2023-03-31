from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from binago.utils import pages_backend
from binago.context_interface import Context

from Events.models import Events

from datetime import datetime
import pytz
import json

from django.utils import timezone


def get_calendar_color(start: datetime, end: datetime):
    now = datetime.today().replace(tzinfo=pytz.UTC)
    start = timezone.localtime(start)
    end = timezone.localtime(end)
    if end.date() < now.date():
        return 'calendar-red'
    if start.date() == now.date() or end.date() == now.date():
        return 'calendar-blue'
    return 'calendar-green'


@login_required
@require_http_methods(['GET'])
def events(request):
    events = Events.objects.all()
    events_collection = []
    for event in events:
        event_start = event.schedule_start.replace(tzinfo=pytz.UTC)
        event_end = event.schedule_end.replace(tzinfo=pytz.UTC)

        events_collection.append({
            'title': event.title,
            'start': str(event.schedule_start),
            'end': str(event.schedule_end),
            'customRender': True,
            'colorStyle': get_calendar_color(event_start, event_end),
        })

    template = pages_backend('dashboard/events.html')
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
        'header': request.user.avatar
    }
    return render(request, template, context)
