from __future__ import annotations
from typing import TYPE_CHECKING

from django.urls import reverse

if TYPE_CHECKING:
    from typing import Literal
    from datetime import datetime

from django.utils import timezone


def timezone_now() -> datetime:
    return timezone.localtime(timezone.now())


def pages_testing(filename) -> str:
    return f"testing/pages/{filename}"


def pages_backend(filename) -> str:
    return f"backend/pages/{filename}"


def pages_frontend(filename) -> str:
    return f"frontend/pages/{filename}"


def pages_mail(filename) -> str:
    return f"mail/{filename}"


def pages_handler(filename) -> str:
    return f"handler/{filename}"


# def homepage_typefilter_reverse(_type: Literal['TODAY', 'UPCOMING', 'PAST'], category: str | Literal[False]) -> str | Literal[False]:
#     if not category:
#         return False
#     if _type == 'TODAY':
#         return reverse('homepage-event-today-category', kwargs={'category': category})
#     if _type == 'UPCOMING':
#         return reverse('homepage-event-upcoming-category', kwargs={'category': category})
#     if _type == 'PAST':
#         return reverse('homepage-event-past-category', kwargs={'category': category})
#     return False
