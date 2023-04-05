from __future__ import annotations
from typing import TYPE_CHECKING

from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

if TYPE_CHECKING:
    from .models import User
    from django.contrib.auth.models import AbstractBaseUser


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: AbstractBaseUser | User, timestamp: int) -> str:
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_verified)
        )


account_activation_token = AccountActivationTokenGenerator()
