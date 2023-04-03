from django.db.models import QuerySet, Count
from django.db.models.fields.files import ImageFieldFile
from typing import Union, List, Any, TypedDict
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect

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
from binago.context_interface import Context


class ContextIndex(Context):
    associations: Union[QuerySet, List[Associations] | List[AssociationsApprovalRequest]]
    members: Any


class ContextInvite(Context):
    form: AssociationInviteForm


class ContextEdit(Context):
    form: AssociationForm


class ContextIndexApproval(Context):
    associations: Union[QuerySet, List[Associations] | List[AssociationsApprovalRequest]]


class Powerheader(TypedDict):
    banner: ImageFieldFile


class ContextProfile(Context):
    association: Union[QuerySet, Associations]
    powerheader: Powerheader
    events: Any
    members: Any


@login_required
@require_http_methods(['GET'])
def index(request) -> HttpResponse:
    template: str = pages_backend('associations/index.html')
    associations: Associations = Associations.objects.get(user=request.user)
    members: Any = associations.associationsgroup_set.filter(is_approved=True).exclude(user=associations.user)
    context: ContextIndex = {
        'title': 'Associations',
        'breadcrumb': {
            'main': 'Associations',
            'branch': [
                {
                    'name': 'Data',
                    'reverse': reverse('associations'),
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
def index_approval(request) -> HttpResponse:
    template: str = pages_backend('associations/approval.html')
    associations = AssociationsApprovalRequest.objects.filter(is_approved=None)
    context: ContextIndexApproval = {
        'title': 'Associations',
        'breadcrumb': {
            'main': 'Associations',
            'branch': [
                {
                    'name': 'Approval',
                    'reverse': reverse('associations-approval'),
                    'type': 'current'
                }
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
    events = association.events_set.all()
    event_categories = association.events_set.values(
        'category', 'category__category').annotate(total=Count('category')).order_by()
    members = association.associationsgroup_set.filter(is_approved=True)
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
    association = get_object_or_404(Associations, user=request.user)
    if request.method == "POST":
        form = AssociationForm(request.POST, request.FILES, instance=association)
        if form.is_valid():
            form.save()

            messages.success(request, 'Association success edited.')
            return redirect('associations-profile')
    else:
        form = AssociationForm(instance=association)

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
    return redirect('associations-approval')


@login_required
@require_http_methods(['POST'])
def approval_reject(request, id) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    approval: AssociationsApprovalRequest = AssociationsApprovalRequest.objects.get(id=id)
    approval.is_approved = False
    approval.save()

    messages.success(request, f'Approval of {approval.associations.name} successfully rejected.')
    return redirect('associations-approval')


@login_required
@require_http_methods(['GET', 'POST'])
def invite(request) -> HttpResponse:
    if request.method == "POST":
        form: AssociationInviteForm = AssociationInviteForm(request.POST)
        association = Associations.objects.filter(user=request.user)
        if form.is_valid():
            user = User.objects.filter(email=form.cleaned_data.get('email'))
            if user.exists() and association.exists():
                invitation, created = AssociationsGroup.objects.get_or_create(
                    user=user.first(),
                    association=association.first()
                )
                if created:
                    messages.success(request, 'Invitation has sent.')
                else:
                    messages.success(request, 'Already sent the invitation.')

            return redirect('associations')
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
                    'reverse': reverse('associations'),
                    'type': 'previous'
                },
                {
                    'name': 'Invite Member',
                    'reverse': reverse('associations-invite'),
                    'type': 'current'
                }
            ]
        },
        'description': 'Your association profile',
        'form': form
    }
    return render(request, template, context)
