from typing import TypedDict, List


class BreadcrumbBranch(TypedDict):
    name: str
    reverse: str


class Breadcrumb(TypedDict):
    main: str
    branch: List[BreadcrumbBranch]


def backend_context(title: str, breadcrumb: Breadcrumb, description: str):
    return {
        'title': title,
        'breadcrumb': breadcrumb,
        'description': description
    }
