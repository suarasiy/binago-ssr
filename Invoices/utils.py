from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Literal, Union
    pass

from .models import InvoiceEventPost, InvoiceUserEventRegistered


def util_adapt_status(status: Literal['settlement', 'pending', 'cancel']) -> Literal["SUCCESS", "FAILED", "WAITING"]:
    if status == "settlement":
        return "SUCCESS"
    if status == "pending":
        return "WAITING"
    if status == "cancel":
        return "FAILED"


def update_status_if_exists(model_name: Literal['invoice_event_post', 'invoice_event_user_register'], order_id: str, transaction_status: Literal['settlement', 'pending', 'cancel']) -> bool:
    status: Literal['SUCCESS', 'FAILED', 'WAITING'] = util_adapt_status(transaction_status)
    if model_name == 'invoice_event_post':
        try:
            invoice_event_publish: InvoiceEventPost = InvoiceEventPost.objects.get(uuid=order_id)
            invoice_event_publish.status = status
            invoice_event_publish.save()
            return True
        except InvoiceEventPost.DoesNotExist:
            return False
    elif model_name == 'invoice_event_user_register':
        try:
            invoice_user_event_register: InvoiceUserEventRegistered = InvoiceUserEventRegistered.objects.get(
                uuid=order_id)
            invoice_user_event_register.status = status
            invoice_user_event_register.save()
            return True
        except InvoiceUserEventRegistered.DoesNotExist:
            return False
    return False
