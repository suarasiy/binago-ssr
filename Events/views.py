from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from binago.utils import pages_backend

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
