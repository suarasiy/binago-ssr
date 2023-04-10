from __future__ import annotations
from typing import TYPE_CHECKING

from django.shortcuts import get_object_or_404
from .models import Associations, AssociationsGroup

if TYPE_CHECKING:
    from django.db.models import QuerySet


def user_registered_associations(request) -> QuerySet[AssociationsGroup]:
    return AssociationsGroup.objects.filter(user=request.user, association__approval__is_approved=True)


def get_association_by_slug(slug) -> Associations:
    return get_object_or_404(Associations, slug=slug)
