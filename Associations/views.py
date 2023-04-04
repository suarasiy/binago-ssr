from __future__ import annotations

from django.db.models import Count
from typing import TYPE_CHECKING

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from Events.models import Events
from authentication.models import User
from .models import Associations, AssociationsGroup, AssociationsApprovalRequest
from .forms import AssociationForm, AssociationInviteForm

from binago.utils import pages_backend

if TYPE_CHECKING:
    from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
    from django.db.models import QuerySet
    from django.db.models.query import ValuesQuerySet
    from .context import (
        ContextIndex, ContextInvite, ContextEdit, ContextIndexApproval, ContextProfile
    )


@login_required
@require_http_methods(['GET'])
def index(request) -> HttpResponse:
    ...


@login_required
@require_http_methods(['GET'])
def index_data(request) -> HttpResponse:
    template: str = pages_backend('associations/index.html')
    associations: Associations = Associations.objects.get(user=request.user)
    members: QuerySet[AssociationsGroup] = associations.associationsgroup_set.filter(
        is_approved=True).exclude(user=associations.user)
    context: ContextIndex = {
        'title': 'Associations',
        'breadcrumb': {
            'main': 'Associations',
            'branch': [
                {
                    'name': 'Data',
                    'reverse': reverse('associations-data'),
                    'type': 'current'
                }
            ]
        },
        'description': 'Manage association members and activity.',
        'associations': Associations.objects.filter(approval__is_approved=True),
        'members': members
    }
    return render(request, template, context)


@login_required
@require_http_methods(['GET'])
def index_data_approval(request) -> HttpResponse:
    template: str = pages_backend('associations/approval.html')
    associations: QuerySet[AssociationsApprovalRequest] = AssociationsApprovalRequest.objects.filter(is_approved=None)
    context: ContextIndexApproval = {
        'title': 'Associations',
        'breadcrumb': {
            'main': 'Associations',
            'branch': [
                {
                    'name': 'Data',
                    'reverse': reverse('associations-data'),
                    'type': 'previous'
                },
                {
                    'name': 'Approval Requests',
                    'reverse': reverse('associations-data-approval'),
                    'type': 'current'
                },
            ]
        },
        'description': 'Associations approval requests.',
        'associations': associations
    }
    return render(request, template, context)


@login_required
@require_http_methods(['GET'])
def profile(request) -> HttpResponse:
    template: str = pages_backend('associations/profile.html')
    association: Associations = Associations.objects.get(user=request.user)
    events: QuerySet[Events] = association.events_set.all()
    event_categories: ValuesQuerySet = association.events_set.values(
        'category', 'category__category').annotate(total=Count('category')).order_by()
    members: QuerySet[AssociationsGroup] = association.associationsgroup_set.filter(is_approved=True)
    context: ContextProfile = {
        'title': 'Associations Profile',
        'breadcrumb': {
            'main': 'Associations',
            'branch': [
                {
                    'name': 'Profile',
                    'reverse': reverse('associations-profile'),
                    'type': 'current'
                }
            ]
        },
        'description': 'Your association profile',
        'association': association,
        'events': events,
        'members': members,
        'events_category': event_categories,
        'powerheader': {
            'banner': association.banner
        }
    }
    return render(request, template, context)


@login_required
@require_http_methods(['GET', 'POST'])
def edit_profile(request) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
    association: Associations = get_object_or_404(Associations, user=request.user)
    if request.method == "POST":
        form: AssociationForm = AssociationForm(request.POST, request.FILES, instance=association)
        if form.is_valid():
            form.save()

            messages.success(request, 'Association success edited.')
            return redirect('associations-profile')
    else:
        form: AssociationForm = AssociationForm(instance=association)

    template: str = pages_backend('associations/edit.html')
    context: ContextEdit = {
        'title': 'Associations | Profile',
        'breadcrumb': {
            'main': 'Associations',
            'branch': [
                {
                    'name': 'Profile',
                    'reverse': reverse('associations-profile'),
                    'type': 'previous'
                },
                {
                    'name': 'Edit',
                    'reverse': reverse('associations-edit'),
                    'type': 'current'
                },
            ]
        },
        'description': 'Update information about your association.',
        'form': form
    }
    return render(request, template, context)


@login_required
@require_http_methods(['POST'])
def approval_accept(request, id) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    approval: AssociationsApprovalRequest = AssociationsApprovalRequest.objects.get(id=id)
    approval.is_approved = True
    approval.save()

    messages.success(request, f'Approval of {approval.associations.name} successfully accepted.')
    return redirect('associations-data-approval')


@login_required
@require_http_methods(['POST'])
def approval_reject(request, id) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    approval: AssociationsApprovalRequest = AssociationsApprovalRequest.objects.get(id=id)
    approval.is_approved = False
    approval.save()

    messages.success(request, f'Approval of {approval.associations.name} successfully rejected.')
    return redirect('associations-data-approval')


@login_required
@require_http_methods(['GET', 'POST'])
def invite(request) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
    if request.method == "POST":
        form: AssociationInviteForm = AssociationInviteForm(request.POST)
        association: QuerySet[Associations] = Associations.objects.filter(user=request.user)
        if form.is_valid():
            user: QuerySet[User] = User.objects.filter(email=form.cleaned_data.get('email'))
            if user.exists() and association.exists():
                _: AssociationsGroup
                created: bool
                _, created = AssociationsGroup.objects.get_or_create(
                    user=user.first(),
                    association=association.first()
                )
                if created:
                    messages.success(request, 'Invitation has sent.')
                else:
                    messages.success(request, 'Already sent the invitation.')

            return redirect('associations-data')
    else:
        form: AssociationInviteForm = AssociationInviteForm()

    template: str = pages_backend('associations/invite.html')
    context: ContextInvite = {
        'title': 'Associations | Invite Member',
        'breadcrumb': {
            'main': 'Associations',
            'branch': [
                {
                    'name': 'Data',
                    'reverse': reverse('associations-data'),
                    'type': 'previous'
                },
                {
                    'name': 'Invite Member',
                    'reverse': reverse('associations-data-invite'),
                    'type': 'current'
                }
            ]
        },
        'description': 'Your association profile',
        'form': form
    }
    return render(request, template, context)
