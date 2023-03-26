from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from binago.utils import pages_backend
from binago.context_interface import backend_context


@login_required
@require_http_methods(['GET'])
def index(request):
    template = pages_backend('organizers/index.html')
    context = backend_context(
        title='Organizers',
        description='Manage your organizers in this page.',
        breadcrumb={
            'main': 'Organizers',
            'branch': [
                {
                    'name': 'Data',
                    'reverse': reverse('organizers'),
                    'type': 'current'
                }
            ]
        }
    )
    return render(request, template, context)
