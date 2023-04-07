from django.core.exceptions import PermissionDenied
from functools import wraps

from .models import Events


def require_association(view):

    @wraps
    def _view(request, *args, **kwargs):
        ...
