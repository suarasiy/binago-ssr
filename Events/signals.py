from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models import QuerySet

from django.dispatch import receiver
from django.core.signals import request_finished
from django.db.models.signals import post_save

from .models import Events
from Invoices.models import InvoiceEventPost


@receiver(post_save, sender=InvoiceEventPost)
def listen_invoice_status(sender, instance, created, *args, **kwargs):
    # check whether the status was changed ['waiting', 'failed', 'success']
    event: Events = instance.event
    invoices: QuerySet[InvoiceEventPost] = InvoiceEventPost.objects.filter(event=event, status='SUCCESS')
    if invoices.exists():
        event.is_published = True
        event.save()
    else:
        if event.is_published == True:
            event.is_published = not event.is_published
            event.save()
