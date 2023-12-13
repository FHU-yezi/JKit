from datetime import datetime
from typing import Optional, Self, Tuple

from jkit._http_client import get_json
from jkit._normalization import normalize_datetime
from jkit._resource_object_base import ResourceObject
from jkit._utils import only_one
from jkit.config import ENDPOINT_CONFIG
from jkit.data_objects.user import (
    GenderEnum,
    MembershipEnum,
    UserBadge,
    UserInfo,
    UserMembership,
)
from jkit.identifier_assert import assert_user_url
from jkit.identifier_convert import user_slug_to_url, user_url_to_slug


# TODO: 用户状态校验
class User(ResourceObject):
    def __init__(
        self, *, url: Optional[str] = None, slug: Optional[str] = None
    ) -> None:
        if not only_one(url, slug):
            raise ValueError("url 和 slug 不可同时提供")

        if url:
            if not assert_user_url(url):
                raise ValueError(f"{url} 不是有效的 user_url")
            self._url = url
        elif slug:
            self._url = user_slug_to_url(slug)
        else:
            raise ValueError("必须提供 url 或 slug")

    @classmethod
    def from_url(cls, url: str, /) -> Self:
        return cls(url=url)

    @classmethod
    def from_slug(cls, slug: str, /) -> Self:
        return cls(slug=slug)

    @property
    def url(self) -> str:
        return self._url

    @property
    def slug(self) -> str:
        return user_url_to_slug(self._url)

    @property
    async def info(self) -> UserInfo:
        data = await get_json(
            endpoint=ENDPOINT_CONFIG.jianshu,
            path=f"/asimov/users/slug/{self.slug}",
        )

        return UserInfo(
            id=data["id"],
            url=user_slug_to_url(data["slug"]),
            slug=data["slug"],
            name=data["nickname"],
            gender={
                0: GenderEnum.UNKNOWN,
                1: GenderEnum.MALE,
                2: GenderEnum.FEMALE,
                3: GenderEnum.UNKNOWN,
            }[data["gender"]],
            introduction=data["intro"],
            introduction_updated_at=normalize_datetime(data["last_updated_at"]),
            avatar_url=data["avatar"],
            background_image_url=data["background_image"],
            badges=tuple(
                UserBadge(
                    name=badge["text"],
                    introduction_url=badge["intro_url"],
                    image_url=badge["image_url"],
                ).validate()
                for badge in data["badges"]
            ),
            membership=UserMembership(
                type=MembershipEnum(
                    data["member"]["type"] if data["member"]["type"] else "none"
                ),
                expired_at=normalize_datetime(data["member"]["expires_at"]),
            ).validate(),
            address_by_ip=data["user_ip_addr"],
            followers_count=data["following_users_count"],
            fans_count=data["followers_count"],
            total_wordage=data["total_wordage"],
            total_likes_count=data["total_likes_count"],
        ).validate()

    @property
    async def id(self) -> int:  # noqa: A003
        return (await self.info).id

    @property
    async def name(self) -> str:
        return (await self.info).name

    @property
    async def gender(self) -> GenderEnum:
        return (await self.info).gender

    @property
    async def introduction(self) -> str:
        return (await self.info).introduction

    @property
    async def introduction_updated_at(self) -> datetime:
        return (await self.info).introduction_updated_at

    @property
    async def avatar_url(self) -> str:
        return (await self.info).avatar_url

    @property
    async def background_image_url(self) -> str:
        return (await self.info).background_image_url

    @property
    async def badges(self) -> Tuple[UserBadge, ...]:
        return (await self.info).badges

    @property
    async def membership(self) -> UserMembership:
        return (await self.info).membership

    @property
    async def address_by_ip(self) -> str:
        return (await self.info).address_by_ip

    @property
    async def followers_count(self) -> int:
        return (await self.info).followers_count

    @property
    async def fans_count(self) -> int:
        return (await self.info).fans_count

    @property
    async def total_wordage(self) -> int:
        return (await self.info).total_wordage

    @property
    async def total_likes_count(self) -> int:
        return (await self.info).total_likes_count
