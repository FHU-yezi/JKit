from collections.abc import Generator
from contextlib import contextmanager

from httpx import HTTPStatusError

from jkit._codec import JSON_DECODER
from jkit.exceptions import ResourceUnavailableError


@contextmanager
def resource_unavaliable_error_handler(*, message: str) -> Generator[None]:
    try:
        yield
    except HTTPStatusError as e:
        if (
            # JSON
            "application/json" in e.response.headers["Content-Type"]
            and "error" in JSON_DECODER.decode(e.response.content)
        ) or (
            # HTML
            "text/html" in e.response.headers["Content-Type"]
            and "<title>您要找的页面不存在 - 简书</title>" in e.response.text
        ):
            raise ResourceUnavailableError(message) from None

        raise
