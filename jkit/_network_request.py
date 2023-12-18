from typing import Any, Dict, Optional

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
