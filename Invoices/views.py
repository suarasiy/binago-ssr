from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
    from . import context
    from django.db.models import QuerySet

from django.core.paginator import Paginator
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from Associations.query import user_registered_associations

from binago.utils import pages_backend
from .models import InvoiceUserEventRegistered


@login_required
@require_http_methods(['GET'])
def index(request) -> HttpResponse:
    page: int = int(request.GET.get('page', 1))
    template: str = pages_backend('invoices/index.html')
    invoices: QuerySet[InvoiceUserEventRegistered] = InvoiceUserEventRegistered.objects.filter(
        event_registered__user=request.user).order_by('-created_at')
    cluster_invoices = Paginator(invoices, 5)
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
        'invoices': cluster_invoices.get_page(page)
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
