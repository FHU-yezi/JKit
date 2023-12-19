from typing import Any, Callable, Coroutine

from jkit.config import BEHAVIOR_CONFIG


def only_one(*args: Any) -> bool:
    return len(tuple(filter(None, args))) == 1


async def validate_if_necessary(
    self_validated: bool, validate_func: Callable[[], Coroutine[None, None, None]], /
) -> None:
    if not BEHAVIOR_CONFIG.auto_validate:
        return

    if not self_validated:
        await validate_func()
