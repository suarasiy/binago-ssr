from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    ...

from django.db import models
from Events.models import Events, EventsUserRegistered
from django.utils import timezone
from datetime import timedelta
from uuid import uuid1


class InvoiceEventPost(models.Model):
    class StatusType(models.TextChoices):
        WAITING = "WAITING", ("Waiting")
        SUCCESS = "SUCCESS", ("Success")
        FAILED = "FAILED", ("Failed")
    id: models.BigIntegerField
    uuid = models.UUIDField(default=uuid1, unique=True)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(default=0)
    status = models.TextField(choices=StatusType.choices, default=StatusType.WAITING)
    midtrans_token = models.CharField(max_length=255, default=None, blank=True, null=True)
    expired_at = models.DateTimeField(default=timezone.now() + timedelta(days=1))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def status_paid(self):
        # NOTE: Procedural hierarchy
        if self.status == "SUCCESS":
            return "PAID"
        if self.status == "WAITING":
            return "WAITING"
        if self.status == "FAILED":
            return "FAILED"

    class Meta:
        verbose_name_plural: str = 'Invoice for Event Publish'
        ordering = ['updated_at']


class InvoiceUserEventRegistered(models.Model):
    class StatusType(models.TextChoices):
        WAITING = "WAITING", ("Waiting")
        SUCCESS = "SUCCESS", ("Success")
        FAILED = "FAILED", ("Failed")
    id: models.BigIntegerField
    uuid = models.UUIDField(default=uuid1, unique=True)
    event_registered = models.ForeignKey(EventsUserRegistered, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(default=0)
    status = models.TextField(choices=StatusType.choices, default=StatusType.WAITING)
    midtrans_token = models.CharField(max_length=255, default=None, blank=True, null=True)
    expired_at = models.DateTimeField(default=timezone.now() + timedelta(days=1))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_discount(self) -> int:
        return round(self.price * (self.discount / 100))

    def status_paid(self):
        # NOTE: Procedural hierarchy
        if self.status == "SUCCESS":
            return "PAID"
        if self.status == "WAITING":
            return "WAITING"
        if self.status == "FAILED":
            return "FAILED"

    def __str__(self) -> str:
        return f'{self.event_registered.user.username} - {self.event_registered.event.title}'

    class Meta:
        verbose_name_plural: str = 'Invoice for User Event Registered'
