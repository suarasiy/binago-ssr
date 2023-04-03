from binago.context_interface import Context
from .forms import UserForm
from .models import User

from django.db.models import QuerySet

from typing import Union


class UserFormContext(Context):
    form: UserForm
    powerheader: Union[QuerySet, User]
