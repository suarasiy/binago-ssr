from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from .models import InvoiceUserEventRegistered
    from binago.context_interface import Context
    from django.core.paginator import Page

    class IndexContext(Context):
        invoices: Page

    class RelatedContext(Context):
        invoices_related: QuerySet[InvoiceUserEventRegistered]
