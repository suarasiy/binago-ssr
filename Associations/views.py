from django.db.models import QuerySet
from typing import Union, List
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect

from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from .models import Associations, AssociationsGroup, AssociationsApprovalRequest
from .forms import AssociationForm

from binago.utils import pages_backend
from binago.context_interface import Context


class ContextIndex(Context):
    associations: Union[QuerySet, List[Associations] | List[AssociationsApprovalRequest]]


@login_required
@require_http_methods(['GET'])
def index(request) -> HttpResponse:
    template: str = pages_backend('associations/index.html')
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
        'associations': Associations.objects.all()
    }
    return render(request, template, context)


@login_required
@require_http_methods(['GET'])
def index_approval(request) -> HttpResponse:
    template: str = pages_backend('associations/approval.html')
    associations = AssociationsApprovalRequest.objects.filter(is_approved=None)
    context: ContextIndex = {
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
@require_http_methods(['POST'])
def approval_accept(request, id) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    approval: AssociationsApprovalRequest = AssociationsApprovalRequest.objects.get(id=id)
    approval.is_approved = True
    approval.save()

    messages.success(request, f'Approval of {approval.association.name} successfully accepted.')
    return redirect('associations-approval')


@login_required
@require_http_methods(['POST'])
def approval_reject(request, id) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    approval: AssociationsApprovalRequest = AssociationsApprovalRequest.objects.get(id=id)
    approval.is_approved = False
    approval.save()

    messages.success(request, f'Approval of {approval.association.name} successfully rejected.')
    return redirect('associations-approval')
