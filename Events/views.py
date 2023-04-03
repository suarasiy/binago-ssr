import json
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect

from binago.utils import pages_backend

from .models import Events, EventsCategories
from .forms import EventForm, EventEditForm


@login_required
@require_http_methods(['GET'])
def index(request):
    template_name = pages_backend('events/index.html')
    events = Events.objects.all()
    context = {
        'title': 'Events',
        'breadcrumb': {
            'main': 'Events',
            'branch': [
                {'name': 'Data', 'reverse': reverse('events')},
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
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.association = request.user.associations
            event.save()

            messages.success(request, 'Event successfully created.')
            return redirect('events')
    else:
        form = EventForm()

    template = pages_backend('events/create.html')
    context = {
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
def events_edit(request, slug):
    event = get_object_or_404(Events, slug=slug)

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()

            messages.success(request, 'Event successfully created.')
            return redirect('events')

    else:
        form = EventForm(instance=event)

    template = pages_backend('events/edit.html')
    context = {
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
def events_destroy(request, slug):
    if request.method == "POST":
        event = get_object_or_404(Events, slug=slug)
        event.delete()

    messages.success(request, 'Event successfully deleted.')
    return redirect('events')
