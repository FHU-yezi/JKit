from typing import Any, Literal, Optional

from httpx import AsyncClient
from httpx._types import ProxiesTypes, TimeoutTypes

from jkit._base import CONFIG_CONFIG, ConfigObject
from jkit._constraints import NonEmptyStr


class _NetworkConfig(ConfigObject, **CONFIG_CONFIG):
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

        import jkit._network_request

        jkit._network_request.HTTP_CLIENT = self._get_http_client()


class _EndpointConfig(ConfigObject, **CONFIG_CONFIG):
    jianshu: NonEmptyStr = "https://www.jianshu.com"


class _BehaviorConfig(ConfigObject, **CONFIG_CONFIG):
    force_validate: bool = True


NETWORK_CONFIG = _NetworkConfig()
ENDPOINT_CONFIG = _EndpointConfig()
BEHAVIOR_CONFIG = _BehaviorConfig()
