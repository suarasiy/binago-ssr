from __future__ import annotations
from typing import TYPE_CHECKING

from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from functools import wraps

# from .models import Events
from authentication.models import User
from Associations.models import Associations, AssociationsGroup, AssociationsApprovalRequest
from django.db.models import Q

if TYPE_CHECKING:
    from typing import Any, Literal
    from django.db.models import QuerySet
    from .models import AssociationsApprovalRequest
    from django.http import Http404
    from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect


def require_association(view) -> None:

    @wraps
    def _view(request, *args, **kwargs) -> None:
        ...


def manager_bypass(request) -> Literal[True] | PermissionDenied:
    user: User = get_object_or_404(User, id=request.user.id)
    if user.is_superuser or user.is_staff:
        return True
    raise PermissionDenied


def permission_staff_only(view):
    @wraps(view)
    def _view(request, *args, **kwargs) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
        user: User = get_object_or_404(User, id=request.user.id)
        if not user.is_staff or not user.is_superuser:
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return _view


def permission_association_manager_only(view):
    @wraps(view)
    def _view(request, *args, **kwargs):
        association: Associations = get_object_or_404(Associations, slug=kwargs.get('slug'))
        user: AssociationsGroup = get_object_or_404(AssociationsGroup, association=association, user=request.user.id)
        if not user.is_manager:
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return _view


def permission_member_specific_association(view):
    @wraps(view)
    def _view(request, *args, **kwargs) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
        user: User = get_object_or_404(User, id=request.user.id)
        association: Associations = get_object_or_404(Associations, slug=kwargs.get('slug'))
        group: QuerySet[AssociationsGroup] = AssociationsGroup.objects.filter(user=user, association=association)
        if not group.exists():
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return _view


def permission_association_is_approved(view):
    @wraps(view)
    def _view(request, *args, **kwargs) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
        if manager_bypass(request):
            return view(request, *args, **kwargs)
        association: Associations = get_object_or_404(Associations, slug=kwargs.get('slug'))
        if not association.approval.is_approved:
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return _view


def permission_association_create_eligibility(view):
    @wraps(view)
    def _view(request, *args, **kwargs) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
        can_action: bool = False if AssociationsApprovalRequest.objects.filter(
            Q(is_approved=None), Q(user=request.user)).exists() else True
        if can_action:
            return view(request, *args, **kwargs)
        raise PermissionDenied
    return _view
