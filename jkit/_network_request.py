from typing import Any, Dict, Optional

from msgspec.json import Decoder

from jkit.config import CONFIG

HTTP_CLIENT = CONFIG.network._get_http_client()
JSON_DECODER = Decoder()


async def get_json(
    *,
    endpoint: str,
    path: str,
    params: Optional[Dict[str, Any]] = None,
    cookies: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    response = await HTTP_CLIENT.get(
        f"{endpoint}{path}",
        params=params,
        cookies=cookies,
    )
    response.raise_for_status()

    return JSON_DECODER.decode(response.content)


async def send_post(
    *,
    endpoint: str,
    path: str,
    params: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, Any]] = None,
    cookies: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    response = await HTTP_CLIENT.post(
        f"{endpoint}{path}",
        params=params,
        json=json,
        headers=headers,
        cookies=cookies,
    )
    response.raise_for_status()

    return JSON_DECODER.decode(response.content)


async def get_html(
    *,
    endpoint: str,
    path: str,
) -> str:
    response = await HTTP_CLIENT.get(f"{endpoint}{path}")
    response.raise_for_status()

    return response.text
