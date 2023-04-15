from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
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
