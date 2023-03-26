import pathlib
from uuid import uuid1
from django.db import models
from django.db.models import SET_NULL, CASCADE
from django.utils.text import slugify
from authentication.models import User
from Organizers.models import *


class EventsCategories(models.Model):
    category = models.CharField(max_length=80, db_index=True, unique=True)
    slug = models.SlugField(unique=True)
    created_by = models.ForeignKey(User, on_delete=SET_NULL, blank=True, null=True)
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
    return f"events/banner/{instance.id}_{fname}{fpath.suffix}"


class Events(models.Model):
    title = models.CharField(max_length=200, db_index=True, unique=True)
    banner = models.ImageField(upload_to=banner_events_upload_handler)
    category = models.ForeignKey(EventsCategories, on_delete=SET_NULL, blank=True, null=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    schedule_start = models.DateTimeField()
    schedule_end = models.DateTimeField()
    url = models.TextField()
    url_youtube = models.TextField(blank=True, null=True)
    url_custom = models.TextField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Events'
        ordering = ['-updated_at']


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
