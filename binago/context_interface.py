from typing import TypedDict, List, Any
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
    forms: ModelForm
