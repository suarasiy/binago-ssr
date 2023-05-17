from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from .models import InvoiceUserEventRegistered, InvoiceEventPost
    from binago.context_interface import Context
    from django.core.paginator import Page

    class IndexContext(Context):
        invoices: Page
        invoices_publish_event: Page
        q_ae: str
        q_pe: str
        midtrans_client_key: str

    class RelatedMidtrans(Context):
        midtrans_client_key: str

    class RelatedContext(RelatedMidtrans):
        invoices_related: QuerySet[InvoiceUserEventRegistered]

    class RelatedContextPublishing(RelatedMidtrans):
        invoices_related: QuerySet[InvoiceEventPost]
