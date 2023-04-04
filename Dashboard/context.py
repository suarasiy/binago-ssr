from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from binago.context import Context as _
    from authentication.models import User

    class Context(_):
        timeline: str
        header: User
