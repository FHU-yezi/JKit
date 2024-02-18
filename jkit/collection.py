from datetime import datetime
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncGenerator,
    Dict,
    List,
    Literal,
    Optional,
)

from httpx import HTTPStatusError
from typing_extensions import Self

from jkit._base import (
    DATA_OBJECT_CONFIG,
    CheckableObject,
    DataObject,
    StandardResourceObject,
)
from jkit._constraints import (
    ArticleSlug,
    CollectionSlug,
    NonEmptyStr,
    NonNegativeFloat,
    NonNegativeInt,
    NormalizedDatetime,
    PositiveInt,
    UserName,
    UserSlug,
    UserUploadedUrl,
)
from jkit._network_request import get_json
from jkit._normalization import normalize_assets_amount, normalize_datetime
from jkit._utils import only_one
from jkit.config import ENDPOINT_CONFIG
from jkit.exceptions import ResourceUnavailableError
from jkit.identifier_check import is_collection_url
from jkit.identifier_convert import collection_slug_to_url, collection_url_to_slug

if TYPE_CHECKING:
    from jkit.article import Article
    from jkit.user import User


class CollectionOwnerInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt
    slug: UserSlug
    name: UserName

    def to_user_obj(self) -> "User":
        from jkit.user import User

        return User.from_slug(self.slug)._as_checked()


class CollectionInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt
    slug: CollectionSlug
    name: NonEmptyStr
    image_url: UserUploadedUrl
    description: str
    description_updated_at: NormalizedDatetime
    new_article_added_at: NormalizedDatetime
    owner_info: CollectionOwnerInfo

    articles_count: NonNegativeInt
    subscribers_count: NonNegativeInt


class CollectionArticleAuthorInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt
    slug: UserSlug
    name: UserName
    avatar_url: UserUploadedUrl

    def to_user_obj(self) -> "User":
        from jkit.user import User

        return User.from_slug(self.slug)._as_checked()


class CollectionArticleInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt
    slug: ArticleSlug
    title: NonEmptyStr
    description: str
    image_url: Optional[UserUploadedUrl]
    published_at: NormalizedDatetime
    is_paid: bool
    can_comment: bool
    author_info: CollectionArticleAuthorInfo

    views_count: NonNegativeInt
    likes_count: NonNegativeInt
    comments_count: NonNegativeInt
    tips_count: NonNegativeInt
    earned_fp_amount: NonNegativeFloat

    def to_article_obj(self) -> "Article":
        from jkit.article import Article

        return Article.from_slug(self.slug)._as_checked()


class Collection(StandardResourceObject, CheckableObject):
    def __init__(
        self, *, url: Optional[str] = None, slug: Optional[str] = None
    ) -> None:
        super().__init__()

        if not only_one(url, slug):
            raise ValueError("专题链接和专题 Slug 不可同时提供")

        if url:
            if not is_collection_url(url):
                raise ValueError(f"{url} 不是有效的专题链接")
            self._url = url
        elif slug:
            self._url = collection_slug_to_url(slug)
        else:
            raise ValueError("必须提供专题链接或专题 Slug")

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

    async def check(self) -> None:
        if self._checked:
            return

        try:
            await get_json(
                endpoint=ENDPOINT_CONFIG.jianshu,
                path=f"/asimov/collections/slug/{self.slug}",
            )
            self._checked = True
        except HTTPStatusError:
            raise ResourceUnavailableError(
                f"专题 {self.url} 不存在或已被删除锁定 / 私密 / 删除"
            ) from None

    @property
    async def info(self) -> CollectionInfo:
        await self._auto_check()

        data = await get_json(
            endpoint=ENDPOINT_CONFIG.jianshu,
            path=f"/asimov/collections/slug/{self.slug}",
        )

        return CollectionInfo(
            id=data["id"],
            slug=data["slug"],
            name=data["title"],
            image_url=data["image"],
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

    @property
    async def name(self) -> str:
        return (await self.info).name

    @property
    async def image_url(self) -> str:
        return (await self.info).image_url

    @property
    async def description(self) -> str:
        return (await self.info).description

    @property
    async def description_updated_at(self) -> datetime:
        return (await self.info).description_updated_at

    @property
    async def new_article_added_at(self) -> datetime:
        return (await self.info).new_article_added_at

    @property
    async def owner_info(self) -> CollectionOwnerInfo:
        return (await self.info).owner_info

    @property
    async def articles_count(self) -> int:
        return (await self.info).articles_count

    @property
    async def subscribers_count(self) -> int:
        return (await self.info).subscribers_count

    async def iter_articles(
        self,
        *,
        start_page: int = 1,
        order_by: Literal["add_time", "last_comment_time", "popularity"] = "add_time",
        page_size: int = 20,
    ) -> AsyncGenerator[CollectionArticleInfo, None]:
        await self._auto_check()

        now_page = start_page
        while True:
            data: List[Dict[str, Any]] = await get_json(
                endpoint=ENDPOINT_CONFIG.jianshu,
                path=f"/asimov/collections/slug/{self.slug}/public_notes",
                params={
                    "page": now_page,
                    "count": page_size,
                    "ordered_by": {
                        "add_time": "time",
                        "last_comment_time": "comment_time",
                        "popularity": "hot",
                    }[order_by],
                },
            )  # type: ignore
            if not data:
                return

            for item in data:
                yield CollectionArticleInfo(
                    id=item["object"]["data"]["id"],
                    slug=item["object"]["data"]["slug"],
                    title=item["object"]["data"]["title"],
                    description=item["object"]["data"]["public_abbr"],
                    image_url=item["object"]["data"]["list_image_url"]
                    if item["object"]["data"]["list_image_url"]
                    else None,
                    published_at=normalize_datetime(
                        item["object"]["data"]["first_shared_at"]
                    ),
                    is_paid=item["object"]["data"]["paid"],
                    can_comment=item["object"]["data"]["commentable"],
                    author_info=CollectionArticleAuthorInfo(
                        id=item["object"]["data"]["user"]["id"],
                        slug=item["object"]["data"]["user"]["slug"],
                        name=item["object"]["data"]["user"]["nickname"],
                        avatar_url=item["object"]["data"]["user"]["avatar"],
                    ),
                    views_count=item["object"]["data"]["views_count"],
                    likes_count=item["object"]["data"]["likes_count"],
                    comments_count=item["object"]["data"]["public_comments_count"],
                    tips_count=item["object"]["data"]["total_rewards_count"],
                    earned_fp_amount=normalize_assets_amount(
                        item["object"]["data"]["total_fp_amount"]
                    ),
                )._validate()

            now_page += 1
