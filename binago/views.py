from .utils import pages_testing, pages_backend
from .context_interface import Context

from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from authentication.models import User
from Associations.models import Associations

from django.db.models import QuerySet
from typing import Union


class SettingsContext(Context):
    powerheader: Union[QuerySet, User]


@login_required
def dashboard(request) -> HttpResponse:
    template_name: str = pages_testing("dashboard.html")
    context = {
        'title': 'testing',
        'user': request.user
    }
    return render(request, template_name, context)


@login_required
@require_http_methods(['GET'])
def settings_profile(request) -> HttpResponse:
    template: str = pages_backend('settings/profile.html')
    user: User = User.objects.get(id=request.user.id)
    context: SettingsContext = {
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
        'powerheader': user
    }
    return render(request, template, context)
