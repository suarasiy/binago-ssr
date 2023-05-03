from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict, List, Union
    from django.forms import ModelForm
    from django.db.models import QuerySet
    from Associations.models import AssociationsGroup
    from .context import QueryFragmentInfoContext

    class BreadcrumbBranch(TypedDict):
        name: str
        reverse: str
        type: str

    class Breadcrumb(TypedDict):
        main: str
        branch: List[BreadcrumbBranch]

    class Context(TypedDict):
        title: str
        breadcrumb: Breadcrumb
        description: str
        registered_associations: Union[QuerySet, List[AssociationsGroup]]

    class ContextHomepage(TypedDict):
        title: str
        description: str
        fragment: QueryFragmentInfoContext
