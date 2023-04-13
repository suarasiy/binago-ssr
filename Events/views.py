from __future__ import annotations
from typing import TYPE_CHECKING

from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from binago.utils import pages_backend
from Associations.query import user_registered_associations, get_association_by_slug

from Associations.models import AssociationsGroup
from Associations.permissions import permission_association_is_approved, permission_member_specific_association

from .models import Events, EventsCoverage
from .forms import EventForm, EventEditForm, EventsCoverageForm
from .utils import list_no_whitespace
if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
    from .context import (
        IndexContext, FormContext
    )
    from typing import Union, List


@login_required
@require_http_methods(['GET'])
def index(request) -> HttpResponse:
    template_name: str = pages_backend('events/index.html')
    events: Union[QuerySet, List[Events]] = Events.objects.all()
    context: IndexContext = {
        'title': 'Events',
        'breadcrumb': {
            'main': 'Events',
            'branch': [
                {
                    'name': 'Data',
                    'reverse': reverse('events'),
                    'type': 'current'
                },
            ]
        },
        'description': 'Manage your events in this page.',
        'events': events,
        'registered_associations': user_registered_associations(request)
    }
    return render(request, template_name, context)


@login_required
@require_http_methods(['GET', 'POST'])
def association_events(request, slug) -> HttpResponse:
    template: str = pages_backend('associations/events.html')
    context: IndexContext = {
        'title': 'Association Event',
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
                    'reverse': reverse('events-association', kwargs={'slug': slug}),
                    'type': 'current'
                }
            ]
        },
        'description': 'Manage your events.',
        'events': Events.objects.all(),
        'registered_associations': user_registered_associations(request)
    }
    return render(request, template, context)

# TODO: Need to improve further since this views is going to the association's urls


@login_required
@require_http_methods(['GET', 'POST'])
@permission_association_is_approved
@permission_member_specific_association
def events_create(request, slug) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
    if request.method == "POST":
        form: EventForm = EventForm(request.POST, request.FILES)
        form_coverage: EventsCoverageForm = EventsCoverageForm(request.POST)
        group: AssociationsGroup = get_object_or_404(
            AssociationsGroup, user=request.user, association=get_association_by_slug(slug))
        if form.is_valid() and form_coverage.is_valid():
            event = form.save(commit=False)
            event.association_group = group
            event.save()

            coverage_list_cleaned: List[str] = list_no_whitespace(
                form_coverage.cleaned_data.get('coverage').split("||"))
            coverage_list_object: List[EventsCoverage] = []
            for coverage in coverage_list_cleaned:
                coverage_list_object.append(EventsCoverage(
                    event=event,
                    coverage=coverage
                ))
            EventsCoverage.objects.bulk_create(coverage_list_object)

            messages.success(request, 'Event successfully created.')
            return redirect(reverse('associations-data-explore', kwargs={'slug': slug}))
    else:
        form: EventForm = EventForm()
        form_coverage: EventsCoverageForm = EventsCoverageForm()

    template: str = pages_backend('events/create.html')
    context: FormContext = {
        'title': 'Associations',
        'breadcrumb': {
            'main': 'Associations',
            'branch': [
                {
                    'name': 'Data',
                    'reverse': reverse('associations-data'),
                    'type': 'previous',
                },
                {
                    'name': get_association_by_slug(slug).name,
                    'reverse': reverse('associations-data-explore', kwargs={'slug': slug}),
                    'type': 'previous',
                },
                {
                    'name': 'New Events',
                    'reverse': reverse('events-create', kwargs={'slug': slug}),
                    'type': 'current'
                }
            ],
        },
        'description': 'One of many gateway to opening knowledge...',
        'forms': form,
        'registered_associations': user_registered_associations(request),
        'slug': slug,
        'forms_coverage': form_coverage
    }
    return render(request, template, context)


@login_required
@require_http_methods(['GET', 'POST'])
@permission_association_is_approved
@permission_member_specific_association
def events_edit(request, slug, slug_event) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
    event: Events = get_object_or_404(Events, slug=slug_event)
    event_coverage: QuerySet[EventsCoverage] = EventsCoverage.objects.filter(event=event)

    if request.method == "POST":
        form: EventEditForm = EventEditForm(request.POST, request.FILES, instance=event)
        form_coverage: EventsCoverageForm = EventsCoverageForm(request.POST)
        # TODO: need to check it again later, afraid occurring some bug
        if form.is_valid() and form_coverage.is_valid():
            form.save()
            EventsCoverage.objects.filter(event=event).delete()

            coverage_list_cleaned: List[str] = list_no_whitespace(
                form_coverage.cleaned_data.get('coverage').split("||"))
            coverage_list_object: List[EventsCoverage] = []
            for coverage in coverage_list_cleaned:
                coverage_list_object.append(EventsCoverage(
                    event=event,
                    coverage=coverage
                ))
            EventsCoverage.objects.bulk_create(coverage_list_object)

            messages.success(request, 'Event successfully created.')
            return redirect(reverse('associations-data-explore', kwargs={'slug': slug}))

    else:
        form: EventEditForm = EventEditForm(instance=event)
        form_coverage: EventsCoverageForm = EventsCoverageForm(data={
            'coverage': " || ".join([obj.coverage for obj in event_coverage])
        })

    template: str = pages_backend('events/edit.html')
    context: FormContext = {
        'title': 'Associations',
        'breadcrumb': {
            'main': 'Associations',
            'branch': [
                {
                    'name': 'Data',
                    'reverse': reverse('associations-data'),
                    'type': 'previous',
                },
                {
                    'name': get_association_by_slug(slug).name,
                    'reverse': reverse('associations-data-explore', kwargs={'slug': slug}),
                    'type': 'previous',
                },
                {
                    'name': event.title,
                    'reverse': request.get_full_path(),
                    'type': 'current'
                }
            ],
        },
        'description': 'One of many gateway to opening knowledge...',
        'forms': form,
        'registered_associations': user_registered_associations(request),
        'slug': slug,
        'forms_coverage': form_coverage
    }

    return render(request, template, context)


@login_required
@require_http_methods(["POST"])
@permission_association_is_approved
@permission_member_specific_association
def events_destroy(request, slug, slug_event) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    if request.method == "POST":
        event: Events = get_object_or_404(Events, slug=slug_event)
        event.delete()

    messages.success(request, 'Event successfully deleted.')
    return redirect(reverse('associations-data-explore', kwargs={'slug': slug}))
