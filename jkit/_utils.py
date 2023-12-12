from typing import Any


def only_one(*args: Any) -> bool:
    return len(tuple(filter(None, args))) == 1
