from __future__ import annotations

from django.db.models import Count, F, Q
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
from .query import user_registered_associations, get_association_by_slug
from .permissions import permission_staff_only, permission_member_specific_association, permission_association_is_approved, permission_association_manager_only, permission_association_create_eligibility

from binago.utils import pages_backend

if TYPE_CHECKING:
    from typing import Union, List
    from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
    from django.db.models import QuerySet
    from django.db.models.query import ValuesQuerySet
    from .context import (
        ContextIndex, ContextInvite, ContextEdit, ContextIndexApproval, ContextProfile, ContextExplore, ContextCreate
    )


@login_required
@require_http_methods(['GET'])
def index(request) -> HttpResponse:
    ...


@login_required
@require_http_methods(['GET'])
@permission_association_is_approved
@permission_member_specific_association
def explore(request, slug) -> HttpResponse:
    template: str = pages_backend('associations/explore.html')
    association: Associations = Associations.objects.get(slug=slug)
    # events: ValuesQuerySet = AssociationsGroup.objects.filter(association=association).values('association__name', 'events__title', 'user__avatar', 'user__first_name', 'user__last_name', 'events__banner', 'events__schedule_start', 'events__schedule_end').annotate().order_by('-events__schedule_end')
    events: QuerySet[Events] = Events.objects.filter(association_group__association=association)
    members: QuerySet[AssociationsGroup] = AssociationsGroup.objects.filter(association=association)
    context: ContextExplore = {
        'title': 'Associations Explore',
        'breadcrumb': {
            'main': 'Associations',
            'branch': [
                {
                    'name': 'Data',
                    'reverse': reverse('associations-data'),
                    'type': 'previous'
                },
                {
                    'name': get_association_by_slug(slug).name,
                    'reverse': reverse('associations-data-explore', kwargs={'slug': slug}),
                    'type': 'current'
                },
            ]
        },
        'association': association,
        'members': members,
        'description': 'Exploring your association!',
        'events': events,
        'registered_associations': user_registered_associations(request)
    }
    return render(request, template, context)


@login_required
@require_http_methods(['GET'])
def index_data(request) -> HttpResponse:
    template: str = pages_backend('associations/index.html')
    # members: QuerySet[AssociationsGroup] = associations.associationsgroup_set.filter(
    #     is_approved=True).exclude(user=associations.user)
    approvals: QuerySet[AssociationsApprovalRequest] = AssociationsApprovalRequest.objects.filter(
        Q(user=request.user)).order_by('-updated_at')

    # PURPOSES: If the user have a 'waiting' list on associations approval requests,
    # ... user can't create another association until approval got an answer.
    associations_create_eligibility: bool = False if AssociationsApprovalRequest.objects.filter(
        Q(is_approved=None), Q(user=request.user)).exists() else True
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
        'members': None,
        'associations_group': user_registered_associations(request),
        'registered_associations': user_registered_associations(request),
        'approvals': approvals,
        'associations_create_eligibility': associations_create_eligibility
    }
    return render(request, template, context)


@login_required
@require_http_methods(['GET'])
@permission_staff_only
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
        'associations': associations,
        'registered_associations': user_registered_associations(request)
    }
    return render(request, template, context)


@login_required
@require_http_methods(['GET'])
@permission_association_is_approved
def profile(request, slug) -> HttpResponse:
    template: str = pages_backend('associations/profile.html')
    association: Associations = Associations.objects.get(slug=slug)
    # events: Any = AssociationsGroup.objects.filter(association=association).prefetch_related('events_set')
    # events: ValuesQuerySet = AssociationsGroup.objects.filter(association=association).values('association__name', 'events__title', 'user__avatar',
    #                                                                                           'user__first_name', 'user__last_name', 'events__banner', 'events__schedule_start', 'events__schedule_end').annotate().order_by('-events__schedule_end')
    # event_categories: ValuesQuerySet = events.values(
    #     'category', 'category__category').annotate(total=Count('category')).order_by()
    events: QuerySet[Events] = Events.objects.filter(association_group__association=association)
    event_categories: ValuesQuerySet = AssociationsGroup.objects.filter(association=association).values(
        'events__category__category').annotate(total=Count('events__category__category'))
    members: QuerySet[AssociationsGroup] = association.associationsgroup_set.filter(is_approved=True)
    context: ContextProfile = {
        'title': 'Associations Profile',
        'breadcrumb': {
            'main': 'Associations',
            'branch': [
                {
                    'name': 'Profile',
                    'reverse': reverse('associations-profile', kwargs={'slug': slug}),
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
        },
        'registered_associations': user_registered_associations(request)
    }
    return render(request, template, context)


@login_required
@require_http_methods(['GET', 'POST'])
@permission_association_create_eligibility
def create(request) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
    if request.method == "POST":
        form: AssociationForm = AssociationForm(request.POST, request.FILES)
        if form.is_valid():
            approval: AssociationsApprovalRequest = AssociationsApprovalRequest.objects.create(
                user=request.user,
            )
            association = form.save(commit=False)
            association.approval = approval
            association.save()
            AssociationsGroup.objects.create(
                association=association,
                user=request.user,
                is_manager=True,
                is_approved=True
            )

            messages.info(
                request, 'Request approval for creating associations succesfully created. We will send the review on your notifications when we\'re done!')
            return redirect('associations-data')
    else:
        form: AssociationForm = AssociationForm()

    template: str = pages_backend('associations/create.html')
    context: ContextCreate = {
        'title': 'Associations | Request to create association',
        'description': 'Create your association and get approved!',
        'breadcrumb': {
            'main': 'Associations',
            'branch': [
                {
                    'name': 'Data',
                    'reverse': reverse('associations-data'),
                    'type': 'previous'
                },
                {
                    'name': 'Request Create Association',
                    'reverse': reverse('associations-create'),
                    'type': 'current'
                },
            ]
        },
        'form': form,
        'registered_associations': user_registered_associations(request)
    }
    return render(request, template, context)


@login_required
@require_http_methods(['GET', 'POST'])
@permission_association_is_approved
@permission_association_manager_only
def edit_profile(request, slug) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
    association: Associations = get_object_or_404(Associations, slug=slug)
    if request.method == "POST":
        form: AssociationForm = AssociationForm(request.POST, request.FILES, instance=association)
        if form.is_valid():
            association: Associations = form.save()

            messages.success(request, 'Association success edited.')
            return redirect(reverse('associations-profile', kwargs={'slug': association.slug}))
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
                    'reverse': reverse('associations-profile', kwargs={'slug': slug}),
                    'type': 'previous'
                },
                {
                    'name': 'Edit',
                    'reverse': reverse('associations-edit', kwargs={'slug': slug}),
                    'type': 'current'
                },
            ]
        },
        'description': 'Update information about your association.',
        'form': form,
        'registered_associations': user_registered_associations(request),
        'slug': slug
    }
    return render(request, template, context)


@login_required
@require_http_methods(['POST'])
@permission_staff_only
def approval_accept(request, id) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    approval: AssociationsApprovalRequest = AssociationsApprovalRequest.objects.get(id=id)
    approval.is_approved = True
    approval.save()

    messages.success(request, f'Approval of {approval.associations.name} successfully accepted.')
    return redirect('associations-data-approval')


@login_required
@require_http_methods(['POST'])
@permission_staff_only
def approval_reject(request, id) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    approval: AssociationsApprovalRequest = AssociationsApprovalRequest.objects.get(id=id)
    approval.is_approved = False
    approval.save()

    messages.success(request, f'Approval of {approval.associations.name} successfully rejected.')
    return redirect('associations-data-approval')


@login_required
@require_http_methods(['GET', 'POST'])
@permission_association_is_approved
@permission_association_manager_only
def invite(request, slug) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
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

            return redirect('associations-data-explore', kwargs={'slug': slug})
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
                    'name': get_association_by_slug(slug).name,
                    'reverse': reverse('associations-data-explore', kwargs={'slug': slug}),
                    'type': 'previous'
                },
                {
                    'name': 'Invite Member',
                    'reverse': reverse('associations-data-invite', kwargs={'slug': slug}),
                    'type': 'current'
                }
            ]
        },
        'description': 'Your association profile',
        'form': form,
        'registered_associations': user_registered_associations(request),
        'slug': slug
    }
    return render(request, template, context)
