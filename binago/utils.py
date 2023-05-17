from __future__ import annotations
from django.utils import timezone
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .context import QueryFragmentInfoContext, UtilSnapContext
    from midtransclient import Snap

import os
from dotenv import load_dotenv
from django.urls import reverse
from midtransclient import Snap

load_dotenv()

if TYPE_CHECKING:
    from typing import Literal
    from datetime import datetime


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


# local payment gateway settings
class SNAP(Snap):
    def __init__(self):
        self.client_key: str = str(os.getenv("MIDTRANS_CLIENT_KEY"))
        self.server_key: str = str(os.getenv("MIDTRANS_SERVER_KEY"))

    def get_client_key(self) -> str:
        return self.client_key

    def get_server_key(self) -> str:
        return self.server_key

    def init_new(self) -> Snap:
        return Snap(
            is_production=False,
            server_key=self.get_server_key()
        )

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
