"""JKit 配置."""

from typing import Any as _Any
from typing import Literal as _Literal
from typing import Optional as _Optional

from httpx import AsyncClient as _AsyncClient
from httpx._types import ProxiesTypes as _ProxiesTypes
from httpx._types import TimeoutTypes as _TimeoutTypes
from msgspec import Struct as _Struct

_CONFIG_CONFIG = {
    "eq": False,
    "kw_only": True,
    "gc": False,
}


class _NetworkConfig(_Struct, **_CONFIG_CONFIG):
    jianshu_base_url: str = "https://www.jianshu.com"
    http_protool: _Literal["HTTP/1", "HTTP/2"] = "HTTP/2"
    proxies: _Optional[_ProxiesTypes] = None
    timeout: _TimeoutTypes = 5

    def _get_http_client(self) -> _AsyncClient:
        return _AsyncClient(
            http1=self.http_protool == "HTTP/1",
            http2=self.http_protool == "HTTP/2",
            proxies=self.proxies,
            timeout=self.timeout,
        )

    def __setattr__(self, __name: str, __value: _Any) -> None:
        super().__setattr__(__name, __value)

        import jkit._http_client
        jkit._http_client.HTTP_CLIENT = self._get_http_client()


NETWORK_CONFIG = _NetworkConfig()
