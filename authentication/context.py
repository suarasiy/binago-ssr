from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from Associations.models import AssociationsGroup
    from django.db.models import QuerySet
    from binago.context_interface import Context
    from .models import User
    from .forms import UserForm

    class UserFormContext(Context):
        form: UserForm
        powerheader: Union[QuerySet, User]

    class IndexContext(Context):
        users: QuerySet[User]

    class ProfileContext(Context):
        powerheader: User
        group: QuerySet[AssociationsGroup]
