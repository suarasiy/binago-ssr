from __future__ import annotations
from typing import TYPE_CHECKING

from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from binago.utils import pages_backend

from .models import Events
from .forms import EventForm
if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
    from .context import (
        IndexContext, FormContext
    )
    from typing import Union, List


@login_required
@require_http_methods(['GET'])
def index(request) -> HttpResponse:
    template_name: str = pages_backend('events/index.html')
    events: Union[QuerySet, List[Events]] = Events.objects.all()
    context: IndexContext = {
        'title': 'Events',
        'breadcrumb': {
            'main': 'Events',
            'branch': [
                {
                    'name': 'Data',
                    'reverse': reverse('events'),
                    'type': 'current'
                },
            ]
        },
        'description': 'Manage your events in this page.',
        'events': events
    }
    return render(request, template_name, context)


@login_required
@require_http_methods(['GET', 'POST'])
def events_create(request) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
    if request.method == "POST":
        form: EventForm = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.association = request.user.associations
            event.save()

            messages.success(request, 'Event successfully created.')
            return redirect('events')
    else:
        form: EventForm = EventForm()

    template: str = pages_backend('events/create.html')
    context: FormContext = {
        'title': 'Events',
        'breadcrumb': {
            'main': 'Events',
            'branch': [
                {
                    'name': 'Data',
                    'reverse': reverse('events'),
                    'type': 'previous',
                },
                {
                    'name': 'New Events',
                    'reverse': reverse('events-create'),
                    'type': 'current'
                }
            ],
        },
        'description': 'One of many gateway to opening knowledge...',
        'forms': form
    }
    return render(request, template, context)


@login_required
@require_http_methods(['GET', 'POST'])
def events_edit(request, slug) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
    event: Events = get_object_or_404(Events, slug=slug)

    if request.method == "POST":
        form: EventForm = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()

            messages.success(request, 'Event successfully created.')
            return redirect('events')

    else:
        form: EventForm = EventForm(instance=event)

    template: str = pages_backend('events/edit.html')
    context: FormContext = {
        'title': 'Events',
        'breadcrumb': {
            'main': 'Events',
            'branch': [
                {
                    'name': 'Data',
                    'reverse': reverse('events'),
                    'type': 'previous',
                },
                {
                    'name': event.title,
                    'reverse': request.get_full_path(),
                    'type': 'current'
                }
            ],
        },
        'description': 'One of many gateway to opening knowledge...',
        'forms': form
    }

    return render(request, template, context)


@login_required
@require_http_methods(["POST"])
def events_destroy(request, slug) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    if request.method == "POST":
        event: Events = get_object_or_404(Events, slug=slug)
        event.delete()

    messages.success(request, 'Event successfully deleted.')
    return redirect('events')
