from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    ...

from django.db import models
from Events.models import Events, EventsUserRegistered


class InvoiceEventPost(models.Model):
    class StatusType(models.TextChoices):
        WAITING = "WAITING", ("Waiting")
        SUCCESS = "SUCCESS", ("Success")
        FAILED = "FAILED", ("Failed")
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=3)
    discount = models.PositiveIntegerField(default=0)
    status = models.TextField(choices=StatusType.choices, default=StatusType.WAITING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural: str = 'Invoice for Event Publish'


class InvoiceUserEventRegistered(models.Model):
    class StatusType(models.TextChoices):
        WAITING = "WAITING", ("Waiting")
        SUCCESS = "SUCCESS", ("Success")
        FAILED = "FAILED", ("Failed")
    event_registered = models.ForeignKey(EventsUserRegistered, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount = models.PositiveIntegerField(default=0)
    status = models.TextField(choices=StatusType.choices, default=StatusType.WAITING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural: str = 'Invoice for User Event Registered'
