"""用户."""
from typing import Optional, Self

from jkit._http_client import HTTP_CLIENT
from jkit._resource_object_base import ResourceObject
from jkit._utils import only_one
from jkit.config import ENDPOINT_CONFIG
from jkit.data_objects.user import UserInfo
from jkit.identifier_convert import user_slug_to_url, user_url_to_slug


class User(ResourceObject):
    """用户类"""

    def __init__(self, url: Optional[str] = None, slug: Optional[str] = None) -> None:
        if not only_one(url, slug):
            raise ValueError("url 和 slug 不可同时提供")

        if url:
            self._url = url
        elif slug:
            self._url = user_slug_to_url(slug)
        else:
            raise ValueError("必须提供 url 或 slug")

    @classmethod
    def from_url(cls, url: str) -> Self:
        return cls(url=url)

    @classmethod
    def from_slug(cls, slug: str) -> Self:
        return cls(slug=slug)

    @property
    def url(self) -> str:
        return self._url

    @property
    def slug(self) -> str:
        return user_url_to_slug(self._url)

    @property
    async def info(self) -> UserInfo:
        response = await HTTP_CLIENT.get(
            f"{ENDPOINT_CONFIG.jianshu}/asimov/users/slug/{self.slug}"
        )
        data = response.json()

        return UserInfo(
            id=data["id"],
            url=user_slug_to_url(data["slug"]),
            slug=data["slug"],
            name=data["nickname"],
            introduction=data["intro"],
        )
