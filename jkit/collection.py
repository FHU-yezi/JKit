from typing import Optional

from httpx import HTTPStatusError
from typing_extensions import Self

from jkit._base import DATA_OBJECT_CONFIG, DataObject, StandardResourceObject
from jkit._constraints import (
    CollectionSlugStr,
    NonEmptyStr,
    NonNegativeInt,
    NormalizedDatetime,
    PositiveInt,
    UserNameStr,
    UserSlugStr,
    UserUploadedUrlStr,
)
from jkit._network_request import get_json
from jkit._normalization import normalize_datetime
from jkit._utils import only_one, validate_if_necessary
from jkit.config import ENDPOINT_CONFIG
from jkit.exceptions import ResourceUnavailableError
from jkit.identifier_check import is_collection_url
from jkit.identifier_convert import collection_slug_to_url, collection_url_to_slug


class CollectionOwnerInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt  # noqa: A003
    slug: UserSlugStr
    name: UserNameStr


class CollectionInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt  # noqa: A003
    slug: CollectionSlugStr
    name: NonEmptyStr
    image: UserUploadedUrlStr
    description: str
    description_updated_at: NormalizedDatetime
    new_article_added_at: NormalizedDatetime
    owner_info: CollectionOwnerInfo

    articles_count: NonNegativeInt
    subscribers_count: NonNegativeInt


class Collection(StandardResourceObject):
    def __init__(self, url: Optional[str] = None, slug: Optional[str] = None) -> None:
        super().__init__()

        if not only_one(url, slug):
            raise ValueError("url 和 slug 不可同时提供")

        if url:
            if not is_collection_url(url):
                raise ValueError(f"{url} 不是有效的 collection_url")
            self._url = url
        elif slug:
            self._url = collection_slug_to_url(slug)
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
        return collection_url_to_slug(self._url)

    async def validate(self) -> None:
        if self._validated:
            return

        try:
            await get_json(
                endpoint=ENDPOINT_CONFIG.jianshu,
                path=f"/asimov/collections/slug/{self.slug}",
            )
            self._validated = True
        except HTTPStatusError:
            raise ResourceUnavailableError(
                f"专题 {self.url} 不存在或已被删除锁定 / 私密 / 删除"
            ) from None

    @property
    async def info(self) -> CollectionInfo:
        await validate_if_necessary(self._validated, self.validate)

        data = await get_json(
            endpoint=ENDPOINT_CONFIG.jianshu,
            path=f"/asimov/collections/slug/{self.slug}",
        )

        return CollectionInfo(
            id=data["id"],
            slug=data["slug"],
            name=data["title"],
            image=data["image"],
            description=data["content_in_full"],
            description_updated_at=normalize_datetime(data["last_updated_at"]),
            new_article_added_at=normalize_datetime(data["newly_added_at"]),
            owner_info=CollectionOwnerInfo(
                id=data["owner"]["id"],
                slug=data["owner"]["slug"],
                name=data["owner"]["nickname"],
            ),
            articles_count=data["notes_count"],
            subscribers_count=data["subscribers_count"],
        )._validate()
