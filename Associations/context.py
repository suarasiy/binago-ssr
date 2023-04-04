from typing import Union, List, Any, TypedDict, TYPE_CHECKING
if TYPE_CHECKING:
    from binago.context_interface import Context
    from Events.models import Events
    from django.db.models import QuerySet
    from django.db.models.fields.files import ImageFieldFile
    from .models import Associations, AssociationsApprovalRequest, AssociationsGroup
    from .forms import AssociationForm, AssociationInviteForm
    from django.db.models.query import ValuesQuerySet

    class ContextIndex(Context):
        associations: Union[QuerySet, List[Associations] | List[AssociationsApprovalRequest]]
        members: Any

    class ContextInvite(Context):
        form: AssociationInviteForm

    class ContextEdit(Context):
        form: AssociationForm

    class ContextIndexApproval(Context):
        associations: Union[QuerySet, List[Associations] | List[AssociationsApprovalRequest]]

    class Powerheader(TypedDict):
        banner: ImageFieldFile

    class ContextProfile(Context):
        association: Union[QuerySet, Associations]
        powerheader: Powerheader
        events: QuerySet[Events]
        members: QuerySet[AssociationsGroup]
        events_category: ValuesQuerySet[Events, dict[str, Any]]
