from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from Invoices.models import InvoiceUserEventRegistered

import pathlib
from uuid import uuid1
from django.db import models
from django.db.models import SET_NULL, CASCADE
from django.utils.text import slugify
from Associations.models import Associations, AssociationsGroup
from authentication.models import User


class EventsCategories(models.Model):
    category = models.CharField(max_length=80, db_index=True, unique=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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


class Events(models.Model):
    association_group = models.ForeignKey(AssociationsGroup, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=200, db_index=True, unique=True)
    banner = models.ImageField(upload_to=banner_events_upload_handler, max_length=500)
    category = models.ForeignKey(EventsCategories, on_delete=SET_NULL, blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True)
    price = models.PositiveIntegerField()
    description = models.TextField()
    schedule_start = models.DateTimeField()
    schedule_end = models.DateTimeField()
    max_audience = models.PositiveIntegerField()
    url_stream = models.TextField()
    url_homepage = models.TextField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Events'
        ordering = ['-created_at']


class EventsExtendedUrl(models.Model):
    event = models.ForeignKey(Events, on_delete=CASCADE)
    url = models.TextField(unique=True)
    url_title = models.CharField(max_length=50, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.url_title} of event {self.event.title}"

    class Meta:
        verbose_name_plural = 'Events Extended url'
        ordering = ['-updated_at']


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
