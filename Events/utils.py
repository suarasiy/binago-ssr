from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List


def list_no_whitespace(n) -> List:
    return [x.strip() for x in n if x.strip()]
