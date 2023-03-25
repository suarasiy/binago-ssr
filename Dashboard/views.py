from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from binago.utils import pages_backend
from binago.context_interface import backend_context


@login_required
@require_http_methods(['GET'])
def events(request):
    template_name = pages_backend('dashboard/events.html')
    context = backend_context(
        'Events',
        {
            'main': 'Overview',
            'branch': [
                {
                    'name': 'Events',
                    'reverse': reverse('dashboard-events')
                },
            ]
        },
        'Here is the summaries about the recent events over the month.'
    )
    return render(request, template_name, context)
