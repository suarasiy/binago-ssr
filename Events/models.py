from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Literal
    from datetime import datetime
    from django.db.models import QuerySet
    from Invoices.models import InvoiceUserEventRegistered, InvoiceEventPost

import pathlib
from uuid import uuid1
from django.db import models
from django.db.models import SET_NULL, CASCADE
from django.utils.text import slugify
from Associations.models import Associations, AssociationsGroup
from authentication.models import User

from .utils import compress_image
from binago.utils import timezone_now
from django.utils import timezone


def builder_count_category_by_schedule_type(_type: Literal['UPCOMING', 'PAST', 'TODAY'], events: QuerySet[Events]) -> QuerySet[Events] | Literal[False]:
    if _type == 'UPCOMING':
        return events.filter(schedule_start__gte=timezone_now())
    if _type == 'PAST':
        return events.filter(schedule_start__lte=timezone_now())
    if _type == 'TODAY':
        return events.filter(schedule_start__month=timezone_now().month, schedule_start__day=timezone_now().day)
    return False


class EventsCategories(models.Model):
    category = models.CharField(max_length=80, db_index=True, unique=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    events_set: QuerySet[Events]

    def get_upcoming_categories(self) -> QuerySet[Events] | Literal[False]:
        return builder_count_category_by_schedule_type('UPCOMING', self.events_set)

    def get_today_categories(self) -> QuerySet[Events] | Literal[False]:
        return builder_count_category_by_schedule_type('TODAY', self.events_set)

    def get_past_categories(self) -> QuerySet[Events] | Literal[False]:
        return builder_count_category_by_schedule_type('PAST', self.events_set)

    def __str__(self):
        return self.category

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Events Categories'


def banner_events_upload_handler(instance, filename):
    fpath = pathlib.Path(filename)
    fname = str(uuid1())
    return f"events/banner/{instance.slug}_{fname}{fpath.suffix}"


def banner_lazy_events_upload_handler(instance, filename):
    fpath = pathlib.Path(filename)
    fname = str(uuid1())
    return f"events/banner/lazy/{instance.slug}_{fname}{fpath.suffix}"


class Events(models.Model):
    id: models.BigIntegerField
    association_group = models.ForeignKey(AssociationsGroup, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=200, db_index=True, unique=True)
    banner = models.ImageField(upload_to=banner_events_upload_handler, max_length=500)
    banner_lazy = models.ImageField(upload_to=banner_lazy_events_upload_handler,
                                    max_length=500, default=None, blank=True, null=True)
    category = models.ForeignKey(EventsCategories, on_delete=SET_NULL, blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True)
    price = models.PositiveIntegerField()
    description = models.TextField()
    schedule_start = models.DateTimeField()
    schedule_end = models.DateTimeField()
    max_audience = models.PositiveIntegerField()
    url_name = models.CharField(max_length=50)
    url_stream = models.TextField()
    url_homepage = models.TextField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user_eligibility: bool
    schedule_eligibility: bool
    seat_eligibility: bool
    invoiceeventpost_set: QuerySet[InvoiceEventPost]
    event_extended_url: QuerySet[EventsExtendedUrl]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        self.banner_lazy = compress_image(self.banner)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def status_paid(self):
        def _(status):
            return self.invoiceeventpost_set.filter(status=status).order_by('-updated_at').first()
        # NOTE: Procedural hierarchy
        if _("SUCCESS"):
            return "PAID"
        if _("WAITING"):
            return "WAITING"
        if _("FAILED"):
            return "FAILED"

    def event_schedule_type(self) -> Literal['TODAY', 'UPCOMING', 'PAST'] | None:
        start: datetime = timezone.localtime(self.schedule_start)
        if start.month == timezone_now().month and start.day == timezone_now().day:
            return "TODAY"
        if start > timezone_now():
            return "UPCOMING"
        if start < timezone_now():
            return "PAST"

    def count_url(self) -> int:
        base_url: Literal[1, 0] = 1 if self.url_stream else 0
        return base_url + self.event_extended_url.all().count()

    class Meta:
        verbose_name_plural = 'Events'
        ordering = ['-created_at']


class EventsExtendedUrl(models.Model):
    event = models.ForeignKey(Events, on_delete=CASCADE, related_name='event_extended_url')
    name = models.CharField(max_length=50, db_index=True)
    url = models.TextField()
    is_attended = models.BooleanField(default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} of event {self.event.title}"

    class Meta:
        verbose_name_plural = 'Events Extended url'
        ordering = ['-updated_at']
        constraints = [
            models.UniqueConstraint(fields=['event', 'name', 'url'], name='unique_event_url')
        ]


class EventsCoverage(models.Model):
    event = models.ForeignKey(Events, on_delete=CASCADE)
    coverage = models.CharField(max_length=80)
    slug = models.SlugField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.coverage, allow_unicode=True)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Events Coverage Outline'
        constraints = [
            models.UniqueConstraint(fields=['event', 'coverage'], name='unique_event_coverage')
        ]


class EventsUserRegistered(models.Model):
    event = models.ForeignKey(Events, on_delete=CASCADE)
    user = models.ForeignKey(User, on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    invoiceusereventregistered_set: QuerySet[InvoiceUserEventRegistered]

    def __str__(self):
        return f'{self.user.username} - {self.event.title}'

    def status_paid(self):
        def _(status):
            return self.invoiceusereventregistered_set.filter(status=status).order_by('-updated_at').first()
        # NOTE: Procedural hierarchy
        if _("SUCCESS"):
            return "PAID"
        if _("WAITING"):
            return "WAITING"
        if _("FAILED"):
            return "FAILED"

    class Meta:
        verbose_name_plural: str = 'Events User Registered'
        constraints = [
            models.UniqueConstraint(fields=['event', 'user'], name='unique_user_registered')
        ]


class EventsAttendee(models.Model):
    user_registered = models.OneToOneField(EventsUserRegistered, on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural: str = 'Events User Attendee'
