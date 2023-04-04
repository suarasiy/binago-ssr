from typing import TypedDict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from django.forms import ModelForm

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
