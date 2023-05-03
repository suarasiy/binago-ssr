from typing import Union, List, Any, TypedDict, TYPE_CHECKING
if TYPE_CHECKING:
    from binago.context_interface import Context
    from django.core.paginator import Page
    from Events.models import Events, EventsExtendedUrl
    from django.db.models import QuerySet
    from django.core.paginator import Page
    from django.db.models.query import ValuesQuerySet
    from django.db.models.fields.files import ImageFieldFile
    from .models import Associations, AssociationsApprovalRequest, AssociationsGroup
    from .forms import AssociationForm, AssociationInviteForm, EventStreamUrlForm
    from django.db.models.query import ValuesQuerySet
    from Events.context import IndexEventResourceContext as IERC

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

    class IndexEventResourceContext(IERC):
        association: Associations

    class StreamFormContext(Context):
        association: Associations
        form: EventStreamUrlForm
        event: Events
        registered_urls: QuerySet[EventsExtendedUrl]

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
