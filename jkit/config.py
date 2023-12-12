from typing import Any, Literal, Optional

from httpx import AsyncClient
from httpx._types import ProxiesTypes, TimeoutTypes
from msgspec import Struct

_CONFIG_CONFIG = {
    "eq": False,
    "kw_only": True,
    "gc": False,
}


class _NetworkConfig(Struct, **_CONFIG_CONFIG):
    http_protool: Literal["HTTP/1", "HTTP/2"] = "HTTP/2"
    proxies: Optional[ProxiesTypes] = None
    timeout: TimeoutTypes = 5

    def _get_http_client(self) -> AsyncClient:
        return AsyncClient(
            http1=self.http_protool == "HTTP/1",
            http2=self.http_protool == "HTTP/2",
            proxies=self.proxies,
            timeout=self.timeout,
        )

    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__setattr__(__name, __value)

        import jkit._http_client

        jkit._http_client.HTTP_CLIENT = self._get_http_client()


class _EndpointConfig(Struct, **_CONFIG_CONFIG):
    jianshu: str = "https://www.jianshu.com"


NETWORK_CONFIG = _NetworkConfig()
ENDPOINT_CONFIG = _EndpointConfig()
