from __future__ import annotations
from typing import TYPE_CHECKING

from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from Associations.query import user_registered_associations

from binago.utils import pages_backend

if TYPE_CHECKING:
    from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
    from .context import IndexContext


@login_required
@require_http_methods(['GET'])
def index(request) -> HttpResponse:
    template: str = pages_backend('users/notification.html')
    context: IndexContext = {
        'title': 'Notification Manager',
        'breadcrumb': {
            'main': 'Users',
            'branch': [
                {
                    'name': 'Notifications',
                    'reverse': reverse('users-notification'),
                    'type': 'current'
                }
            ]
        },
        'description': 'All notifications shown here.',
        'registered_associations': user_registered_associations(request),
    }
    return render(request, template, context)
