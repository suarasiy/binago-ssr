from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from binago.utils import pages_backend
from binago.context_interface import backend_context

from .models import *


@login_required
@require_http_methods(["GET"])
def index(request):
    template_name = pages_backend('events/index.html')
    context = {
        'title': 'Events',
        'breadcrumb': {
            'main': 'Events',
            'branch': [
                {'name': 'Data', 'reverse': reverse('events')},
            ]
        },
        'description': 'Manage your events in this page.'
    }
    return render(request, template_name, context)


@login_required
@require_http_methods(['GET'])
def events_create(request):
    template = pages_backend('events/create.html')
    context = backend_context(
        'Events',
        {
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
            ]
        },
        'One of many gateway to opening knowledge...'
    )
    return render(request, template, context)
