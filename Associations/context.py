from typing import Union, List, Any, TypedDict, TYPE_CHECKING
if TYPE_CHECKING:
    from binago.context_interface import Context
    from django.core.paginator import Page
    from Events.models import Events
    from django.db.models import QuerySet
    from django.core.paginator import Page
    from django.db.models.query import ValuesQuerySet
    from django.db.models.fields.files import ImageFieldFile
    from .models import Associations, AssociationsApprovalRequest, AssociationsGroup
    from .forms import AssociationForm, AssociationInviteForm
    from django.db.models.query import ValuesQuerySet

    class ContextIndex(Context):
        associations: Page
        associations_group: Union[QuerySet, List[AssociationsGroup]]
        members: Any
        approvals: Page
        associations_create_eligibility: bool

    class ContextExplore(Context):
        events: Page
        association: Associations
        members: Page
        q_events: str
        q_members: str

    class ContextInvite(Context):
        slug: str
        form: AssociationInviteForm

    class ContextEdit(Context):
        form: AssociationForm
        slug: str

    class ContextCreate(Context):
        form: AssociationForm

    class ContextIndexApproval(Context):
        associations: Page

    class Powerheader(TypedDict):
        banner: ImageFieldFile

    class ContextProfile(Context):
        association: Union[QuerySet, Associations]
        powerheader: Powerheader
        events: Page
        members: QuerySet[AssociationsGroup]
        events_category: ValuesQuerySet
        has_member: bool
        # events_category: ValuesQuerySet[Events, dict[str, Any]]
