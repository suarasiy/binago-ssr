from django.db import models
from django.db.models import CASCADE
from django.utils.text import slugify

import pathlib
from uuid import uuid1

from authentication.models import User


def logo_upload_handler(instance, filename):
    fpath = pathlib.Path(filename)
    fname = str(uuid1())
    return f"associations/logo/{instance.slug}_{fname}{fpath.suffix}"


def banner_upload_handler(instance, filename):
    fpath = pathlib.Path(filename)
    fname = str(uuid1())
    return f"associations/banner/{instance.slug}_{fname}{fpath.suffix}"


class Associations(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    location = models.CharField(max_length=100)
    about = models.TextField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    logo = models.ImageField(upload_to=logo_upload_handler)
    banner = models.ImageField(upload_to=banner_upload_handler)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Associations'


class AssociationsGroup(models.Model):
    association = models.ForeignKey(Associations, on_delete=CASCADE)
    user = models.ForeignKey(User, on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Associations Group'
        constraints = [
            models.UniqueConstraint(fields=['association', 'user'], name='unique_user_association')
        ]


class AssociationsApprovalRequest(models.Model):
    association = models.OneToOneField(Associations, on_delete=CASCADE)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.association.user} - {self.association}"

    class Meta:
        verbose_name_plural = 'Associations Approval Request'
