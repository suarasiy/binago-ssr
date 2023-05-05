from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import pathlib
from uuid import uuid1


def user_avatar_upload_handler(instance, filename) -> str:
    fpath = pathlib.Path(filename)
    fname = str(uuid1())
    return f"user/avatar/{instance.id}__{fname}{fpath.suffix}"


def user_banner_upload_handler(instance, filename) -> str:
    fpath = pathlib.Path(filename)
    fname = str(uuid1())
    return f"user/banner/{instance.id}__{fname}{fpath.suffix}"


class UserManager(BaseUserManager):

    def create_user(self, username, email, password):
        if username is None:
            raise TypeError("Users required.")

        if email is None:
            raise TypeError("Email required.")

        if password is None:
            raise TypeError("Password required.")

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_verified = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    class Gender(models.TextChoices):
        MALE = "M", ("Male")
        FEMALE = "F", ("Female")
        HIDE = "H", ("Hide Gender")

    username = models.CharField(max_length=100, unique=True, db_index=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    about = models.TextField(default=None, blank=True, null=True)
    avatar = models.ImageField(upload_to=user_avatar_upload_handler, blank=True, null=True)
    banner = models.ImageField(upload_to=user_banner_upload_handler, blank=True, null=True)
    gender = models.TextField(max_length=1, choices=Gender.choices, default=Gender.HIDE)
    institute = models.CharField(max_length=50, default=None, blank=True, null=True)
    city = models.CharField(max_length=50, default=None, blank=True, null=True)
    is_developer = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def is_manager_bypass(self) -> bool:
        if self.is_superuser or self.is_staff:
            return True
        return False

    def avatar_preview(self):
        return mark_safe(
            f"""
            <img src="{self.avatar.url}" width="120" height="120" style="object-fit: cover; object-position: center; border-radius: 15px; margin-right: 5px;" />
            <img src="{self.banner.url}" width="180" height="120" style="object-fit: cover; object-position: center; border-radius: 15px;" />
            """
        )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "User"
        ordering = ['-created_at']
