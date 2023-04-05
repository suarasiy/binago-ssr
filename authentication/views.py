from __future__ import annotations
from typing import TYPE_CHECKING

from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from binago.utils import pages_backend, pages_frontend
from .models import User
from .forms import UserForm, LoginForm, RegisterForm
from .utils import activate_email, verify

if TYPE_CHECKING:
    from typing import Any, Union
    from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
    from .context import (
        UserFormContext
    )
    from django.contrib.auth.models import AbstractBaseUser


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
        'powerheader': user
    }
    return render(request, template, context)
