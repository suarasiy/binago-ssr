from __future__ import annotations
from typing import TYPE_CHECKING

from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404

from authentication.models import User

from functools import wraps

if TYPE_CHECKING:
    from typing import Literal
    from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect


def manager_bypass(request) -> bool:
    user: User = get_object_or_404(User, id=request.user.id)
    if user.is_superuser or user.is_staff:
        return True
    return False


def permission_staff_only(view):
    @wraps(view)
    def _view(request, *args, **kwargs) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
        user: User = get_object_or_404(User, id=request.user.id)
        if not user.is_staff or not user.is_superuser:
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return _view
