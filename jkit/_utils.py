from typing import Callable, Coroutine

from jkit.config import RESOURCE_OBJECT_CONFIG


def only_one(*args: object) -> bool:
    return len(tuple(filter(None, args))) == 1


async def check_if_necessary(
    self_checked: bool, check_func: Callable[[], Coroutine[None, None, None]], /
) -> None:
    if not RESOURCE_OBJECT_CONFIG.auto_checking:
        return

    if not self_checked:
        await check_func()
