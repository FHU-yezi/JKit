from typing import Any, Dict, Optional

from lxml.html import HtmlElement
from lxml.html import fromstring as parse_html
from msgspec.json import Decoder

from jkit.config import NETWORK_CONFIG

HTTP_CLIENT = NETWORK_CONFIG._get_http_client()
JSON_DECODER = Decoder()


async def get_json(
    *,
    endpoint: str,
    path: str,
    params: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    response = await HTTP_CLIENT.get(f"{endpoint}{path}", params=params)
    response.raise_for_status()

    return JSON_DECODER.decode(response.content)


async def get_html(
    *,
    endpoint: str,
    path: str,
) -> HtmlElement:
    response = await HTTP_CLIENT.get(f"{endpoint}{path}")
    response.raise_for_status()

    return parse_html(response.content)
