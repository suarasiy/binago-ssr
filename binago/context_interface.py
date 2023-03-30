from typing import TypedDict, List, Any


class BreadcrumbBranch(TypedDict):
    name: str
    reverse: str
    type: str


class Breadcrumb(TypedDict):
    main: str
    branch: List[BreadcrumbBranch]


def backend_context(title: str, breadcrumb: Breadcrumb, description: str, forms):
    return {
        'title': title,
        'breadcrumb': breadcrumb,
        'description': description,
        'forms': forms,
    }
