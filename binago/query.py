from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from binago.context_interface import QueryFragmentInfoContext

from authentication.query import count_verified_users
from Associations.query import count_verified_associations
from Events.query import count_verified_events


def fragment_info() -> QueryFragmentInfoContext:
    return {
        'registered_users': count_verified_users(),
        'registered_associations': count_verified_associations(),
        'registered_events': count_verified_events()
    }
