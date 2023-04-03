from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from binago.context_interface import Context
from binago.utils import pages_backend
from .models import User
from .forms import UserForm
from .context import UserFormContext


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
