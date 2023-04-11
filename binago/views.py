from __future__ import annotations
from typing import TYPE_CHECKING

from .utils import pages_testing, pages_backend, pages_frontend, pages_handler

from django.urls import reverse
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from authentication.models import User
from Associations.query import user_registered_associations

from Events.models import Events

if TYPE_CHECKING:
    from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
    from .context import (
        SettingsContext, HomepageContext, EventDetailContext
    )


@require_http_methods(['GET'])
def homepage(request) -> HttpResponse:
    template: str = pages_frontend('homepage/index.html')
    context: HomepageContext = {
        'title': 'Binago homepage',
        'description': 'Explore the events.',
        'events': Events.objects.all().order_by('-schedule_start')
    }
    return render(request, template, context)


@require_http_methods(['GET'])
def event_detail(request, slug) -> HttpResponse:
    template: str = pages_frontend('homepage/event_detail.html')
    context: EventDetailContext = {
        'title': 'Binago Events Detail',
        'description': 'Detail the events.',
        'event': get_object_or_404(Events, slug=slug)
    }
    return render(request, template, context)


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


# TODO: change before production
def handle_403(request):
    template = 'handler/403.html'
    context = {}
    return render(request, template, context)


# TODO: change before production
def handle_404(request):
    template = 'handler/404.html'
    context = {}
    return render(request, template, context)


# TODO: change before production
def handle_500(request):
    template = 'handler/500.html'
    context = {}
    return render(request, template, context)
