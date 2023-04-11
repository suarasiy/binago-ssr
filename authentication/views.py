from __future__ import annotations
from typing import TYPE_CHECKING

from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from binago.utils import pages_backend, pages_frontend
from .models import User
from .forms import UserForm, LoginForm, RegisterForm
from .utils import activate_email, verify
from .permissions import permission_staff_only

from Associations.query import user_registered_associations
from Associations.models import AssociationsGroup

if TYPE_CHECKING:
    from typing import Any, Union, Literal
    from django.db.models import QuerySet
    from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
    from .context import (
        UserFormContext, IndexContext, ProfileContext
    )
    from django.contrib.auth.models import AbstractBaseUser


@login_required
@require_http_methods(['GET'])
def index(request) -> HttpResponse:
    ...


@login_required
@require_http_methods(['GET'])
@permission_staff_only
def index_data(request) -> HttpResponse:
    template: str = pages_backend('users/index.html')
    users: QuerySet[User] = User.objects.all()
    context: IndexContext = {
        'title': 'Users data',
        'breadcrumb': {
            'main': 'Users',
            'branch': [
                {
                    'name': 'Data',
                    'reverse': '',
                    'type': 'current'
                }
            ]
        },
        'users': users,
        'description': 'List of registered users.',
        'registered_associations': user_registered_associations(request)
    }
    return render(request, template, context)


@login_required
@require_http_methods(['POST'])
@permission_staff_only
def enable_disable_account(request, id) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    user: User = get_object_or_404(User, id=id)
    user.is_active = not user.is_active
    user.save()

    status: Literal['Activated', 'Disabled'] = "Activated" if user.is_active else "Disabled"
    messages.success(request, f"User successfully {status}.")
    return redirect('users-data')


@require_http_methods(['GET', 'POST'])
def signin(request) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
    if request.user.is_authenticated:
        return redirect('dashboard-events')  # TODO: change it later

    if request.method == "POST":
        form: LoginForm = LoginForm(request.POST)
        if form.is_valid():
            email: str = form.cleaned_data.get('email')
            password: str = form.cleaned_data.get('password')
            # attempt to login
            user: AbstractBaseUser | None = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                _next: str = request.GET.get('next')
                if _next:
                    return redirect(_next)

                return redirect('dashboard-events')  # TODO: change it later

            messages.error(request, 'Email or password is invalid. Please try again.')
    else:
        form: LoginForm = LoginForm()

    template: str = pages_frontend('authentication/login.html')
    context: Any = {
        'form': form
    }
    return render(request, template, context)


@require_http_methods(['GET', 'POST'])
def register(request) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
    if request.user.is_authenticated:
        return redirect('dashboard-events')

    if request.method == "POST":
        form: Union[RegisterForm, AbstractBaseUser] = RegisterForm(request.POST)
        if form.is_valid():
            password: str = form.cleaned_data.get('password')
            user: User = form.save(commit=False)
            user.set_password(password)
            user.save()

            # messages.success(request, 'Account has successfully created. Please check your email to verify your account.')
            activate_email(request, user, user.email)
            return redirect('login')
    else:
        form = RegisterForm()

    template: str = pages_frontend('authentication/register.html')
    context: Any = {
        'form': form
    }
    return render(request, template, context)


@require_http_methods(['GET'])
def verify_account(request, uidb64, token) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    return verify(request, uidb64, token)


# TODO: need to work
@require_http_methods(['GET'])
def request_verify_account(request) -> HttpResponse:
    return render(request, "Mantap :'v")


@login_required
@require_http_methods(['GET', 'POST'])
def edit(request) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
    user: User = get_object_or_404(User, id=request.user.id)
    if request.method == "POST":
        form: UserForm = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()

            messages.success(request, 'Profile has been updated.')
            return redirect('settings')
    else:
        form: UserForm = UserForm(instance=user)

    template: str = pages_backend('users/edit.html')
    context: UserFormContext = {
        'title': 'Profiles | Edit',
        'breadcrumb': {
            'main': 'Settings',
            'branch': [
                {
                    'name': 'Profile',
                    'reverse': reverse('settings'),
                    'type': 'previous'
                },
                {
                    'name': 'Edit',
                    'reverse': reverse('settings-edit'),
                    'type': 'current'
                }
            ]
        },
        'description': 'Update profile information',
        'form': form,
        'powerheader': user,
        'registered_associations': user_registered_associations(request)
    }
    return render(request, template, context)


@login_required
@require_http_methods(['GET'])
def profile(request, username) -> HttpResponse:
    template: str = pages_backend('users/profile.html')
    user: User = get_object_or_404(User, username=username)
    group: QuerySet[AssociationsGroup] = AssociationsGroup.objects.filter(
        Q(user=user), Q(association__approval__is_approved=True))
    context: ProfileContext = {
        'title': f'Profiles | {user.username}\'s profile',
        'breadcrumb': {
            'main': 'Users',
            'branch': [
                {
                    'name': 'Data',
                    'reverse': reverse('users-data'),
                    'type': 'previous'
                },
                {
                    'name': user.username,
                    'reverse': reverse('users-profile', kwargs={'username': username}),
                    'type': 'current'
                }
            ]
        },
        'description': 'Previewing profile.',
        'registered_associations': user_registered_associations(request),
        'powerheader': user,
        'group': group
    }
    return render(request, template, context)
