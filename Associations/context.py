from typing import Union, List, Any, TypedDict, TYPE_CHECKING
if TYPE_CHECKING:
    from binago.context_interface import Context
    from Events.models import Events
    from django.db.models import QuerySet
    from django.db.models.query import ValuesQuerySet
    from django.db.models.fields.files import ImageFieldFile
    from .models import Associations, AssociationsApprovalRequest, AssociationsGroup
    from .forms import AssociationForm, AssociationInviteForm
    from django.db.models.query import ValuesQuerySet

    class ContextIndex(Context):
        associations: Union[QuerySet, List[Associations] | List[AssociationsApprovalRequest]]
        associations_group: Union[QuerySet, List[AssociationsGroup]]
        members: Any
        approvals: QuerySet[AssociationsApprovalRequest]
        associations_create_eligibility: bool

    class ContextExplore(Context):
        events: QuerySet[Events]
        association: Associations
        members: Union[QuerySet, List[AssociationsGroup]]

    class ContextInvite(Context):
        slug: str
        form: AssociationInviteForm

    class ContextEdit(Context):
        form: AssociationForm
        slug: str

    class ContextCreate(Context):
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
        events_category: ValuesQuerySet
        # events_category: ValuesQuerySet[Events, dict[str, Any]]
