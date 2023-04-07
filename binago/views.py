from __future__ import annotations
from typing import TYPE_CHECKING

from .utils import pages_testing, pages_backend, pages_frontend

from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from authentication.models import User
from Associations.query import user_registered_associations

if TYPE_CHECKING:
    from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
    from .context import (
        SettingsContext
    )


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
        'powerheader': user,
        'registered_associations': user_registered_associations(request)
    }
    return render(request, template, context)


@require_http_methods(['GET'])
def signin(request) -> HttpResponse:
    template: str = pages_frontend('authentication/login.html')
    context: dict = {}
    return render(request, template, context)


@login_required
@require_http_methods(['POST'])
def signout(request) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    logout(request)
    return redirect('login')  # TODO: change it later
