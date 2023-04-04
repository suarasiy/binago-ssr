from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from binago.context_interface import Context
    from .models import User
    from .forms import UserForm

    class UserFormContext(Context):
        form: UserForm
        powerheader: Union[QuerySet, User]
