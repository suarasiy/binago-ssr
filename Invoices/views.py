from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Literal
    from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
    from . import context
    from django.db.models import QuerySet

import json
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.http.response import JsonResponse

from Associations.query import user_registered_associations

from binago.utils import pages_backend, SNAP
from Events.models import Events
from .models import InvoiceUserEventRegistered, InvoiceEventPost
from .utils import update_status_if_exists

from django.views.decorators.csrf import csrf_exempt


@login_required
@require_http_methods(['GET'])
def index(request) -> HttpResponse:
    snap = SNAP()
    page_ae: int = int(request.GET.get('page_ae', 1))
    page_pe: int = int(request.GET.get('page_pe', 1))

    ae: str | Literal[False] = request.GET.get('page_ae', False)
    pe: str | Literal[False] = request.GET.get('page_pe', False)

    build_ae: str = f'&page_ae={page_ae}' if ae else ''
    build_pe: str = f'&page_pe={page_pe}' if pe else ''

    template: str = pages_backend('invoices/index.html')
    invoices: QuerySet[InvoiceUserEventRegistered] = InvoiceUserEventRegistered.objects.filter(
        event_registered__user=request.user).order_by('-created_at')
    invoices_publish_events: QuerySet[InvoiceEventPost] = InvoiceEventPost.objects.filter(
        Q(event__association_group__user=request.user)
    ).order_by('-created_at')
    cluster_invoices = Paginator(invoices, 5)
    cluster_invoices_pe = Paginator(invoices_publish_events, 5)
    context: context.IndexContext = {
        'title': 'Invoices',
        'breadcrumb': {
            'main': 'Invoices',
            'branch': [
                {
                    'name': 'Data',
                    'reverse': reverse('invoices'),
                    'type': 'current'
                }
            ]
        },
        'description': 'Listing invoices.',
        'registered_associations': user_registered_associations(request),
        'invoices': cluster_invoices.get_page(page_ae),
        'invoices_publish_event': cluster_invoices_pe.get_page(page_pe),
        'q_ae': build_ae,
        'q_pe': build_pe,
        'midtrans_client_key': snap.get_client_key()
    }
    return render(request, template, context)


@login_required
@require_http_methods(['POST'])
def cancel_invoices(request, id) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    invoice: InvoiceUserEventRegistered = get_object_or_404(InvoiceUserEventRegistered, id=id)
    invoice.status = "FAILED"
    invoice.save()

    messages.success(request, f'Invoices for {invoice.event_registered.event.title} successfully canceled.')
    return redirect(reverse('invoices'))


@login_required
@require_http_methods(['GET'])
def related_invoices(request, event_id) -> HttpResponse:
    # invoices: InvoiceUserEventRegistered = get_object_or_404(InvoiceUserEventRegistered, id=pk)
    event: Events = get_object_or_404(Events, id=event_id)
    invoices_related: QuerySet[InvoiceUserEventRegistered] = InvoiceUserEventRegistered.objects.filter(
        event_registered__event__id=event_id, event_registered__user__id=request.user.id).order_by('-created_at')
    template: str = pages_backend('invoices/related.html')
    context: context.RelatedContext = {
        'title': 'Binago Dashboard | Invoices Event Related',
        'breadcrumb': {
            'main': 'Invoices',
            'branch': [
                {
                    'name': 'Data',
                    'reverse': reverse('invoices'),
                    'type': 'previous'
                },
                {
                    'name': f'Listing invoices of {event.title}',
                    'reverse': reverse('invoices-related', kwargs={'event_id': event_id}),
                    'type': 'current'
                }
            ]
        },
        'description': 'Listing of invoices that you\'ve made for this events.',
        'invoices_related': invoices_related,
        'registered_associations': user_registered_associations(request),
        'midtrans_client_key': SNAP().get_client_key()
    }
    return render(request, template, context)


@login_required
@require_http_methods(['GET'])
def related_invoices_p(request, event_id) -> HttpResponse:
    template: str = pages_backend('invoices/related_for_publish.html')
    event: Events = get_object_or_404(Events, id=event_id)
    invoices_related: QuerySet[InvoiceEventPost] = InvoiceEventPost.objects.filter(
        event__id=event_id).order_by('-created_at')
    context: context.RelatedContextPublishing = {
        'title': 'Binago Dashboard | Invoices Publishing Related',
        'breadcrumb': {
            'main': 'Invoices',
            'branch': [
                {
                    'name': 'Data',
                    'reverse': reverse('invoices'),
                    'type': 'previous'
                },
                {
                    'name': f'Listing invoices of {event.title}',
                    'reverse': reverse('invoices'),
                    'type': 'current'
                },
            ]
        },
        'description': 'Listing of invoices that you\'ve made for this events.',
        'invoices_related': invoices_related,
        'registered_associations': user_registered_associations(request),
        'midtrans_client_key': SNAP().get_client_key()
    }
    return render(request, template, context)


@csrf_exempt
@require_http_methods(['POST'])
def update_payment_status(request):
    # webhook to handle invoices status
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    # get attr request
    status_code: int = int(body.get('status_code'))
    transaction_status: Literal['pending', 'cancel', 'settlement'] = body.get('transaction_status')
    order_id: str = body.get('order_id')

    if status_code == 200:
        # TODO: need to improve, it's already doing update action tho
        if update_status_if_exists('invoice_event_post', order_id, transaction_status):
            pass
        elif update_status_if_exists('invoice_event_user_register', order_id, transaction_status):
            pass

    return JsonResponse(body)
