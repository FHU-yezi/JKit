from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional

from httpx import HTTPStatusError
from typing_extensions import Self

from jkit._base import DATA_OBJECT_CONFIG, DataObject, StandardResourceObject
from jkit._constraints import (
    NonEmptyStr,
    NonNegativeFloat,
    NonNegativeInt,
    NormalizedDatetime,
    Percentage,
    PositiveFloat,
    PositiveInt,
    UserNameStr,
    UserSlugStr,
    UserUploadedUrlStr,
)
from jkit._network_request import get_json
from jkit._normalization import normalize_assets_amount, normalize_datetime
from jkit._utils import only_one, validate_if_necessary
from jkit.config import ENDPOINT_CONFIG
from jkit.exceptions import ResourceUnavailableError
from jkit.identifier_check import is_article_url
from jkit.identifier_convert import article_slug_to_url, article_url_to_slug

if TYPE_CHECKING:
    from jkit.user import User


class NotebookPaidStatusEnum(Enum):
    FREE = "免费"
    PAID = "付费"


class ArticlePaidStatusEnum(Enum):
    FREE = "免费"
    PAID = "付费"


class ArticlePaidInfo(DataObject, **DATA_OBJECT_CONFIG):
    notebook_paid_status: Optional[NotebookPaidStatusEnum]
    article_paid_status: ArticlePaidStatusEnum
    price: Optional[PositiveFloat]
    paid_cotent_percent: Optional[Percentage]
    paid_readers_count: Optional[NonNegativeInt]


class ArticleUserInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt  # noqa: A003
    slug: UserSlugStr
    name: UserNameStr
    avatar_url: UserUploadedUrlStr
    introduction: str
    address_by_ip: NonEmptyStr

    total_wordage: NonNegativeInt
    total_likes_count: NonNegativeInt

    @property
    def get_user_obj(self) -> "User":
        from jkit.user import User

        return User.from_slug(self.slug)


class ArticleInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt  # noqa: A003
    notebook_id: PositiveInt
    title: NonEmptyStr
    description: NonEmptyStr
    wordage: PositiveInt
    published_at: NormalizedDatetime
    updated_at: NormalizedDatetime
    can_comment: bool
    can_reprint: bool
    paid_info: ArticlePaidInfo
    user_info: ArticleUserInfo
    content: NonEmptyStr

    likes_count: NonNegativeInt
    comments_count: NonNegativeInt
    featured_comments_count: NonNegativeInt
    earned_fp_amount: NonNegativeFloat


class Article(StandardResourceObject):
    def __init__(
        self, *, url: Optional[str] = None, slug: Optional[str] = None
    ) -> None:
        super().__init__()

        if not only_one(url, slug):
            raise ValueError("url 和 slug 不可同时提供")

        if url:
            if not is_article_url(url):
                raise ValueError(f"{url} 不是有效的 article_url")
            self._url = url
        elif slug:
            self._url = article_slug_to_url(slug)
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
        return article_url_to_slug(self._url)

    async def validate(self) -> None:
        if self._validated:
            return

        try:
            await get_json(
                endpoint=ENDPOINT_CONFIG.jianshu,
                path=f"/asimov/p/{self.slug}",
            )
            self._validated = True
        except HTTPStatusError:
            raise ResourceUnavailableError(
                f"文章 {self.url} 不存在或已被锁定 / 私密 / 删除"
            ) from None

    @property
    async def info(self) -> ArticleInfo:
        await validate_if_necessary(self._validated, self.validate)

        data = await get_json(
            endpoint=ENDPOINT_CONFIG.jianshu,
            path=f"/asimov/p/{self.slug}",
        )

        return ArticleInfo(
            id=data["id"],
            notebook_id=data["notebook_id"],
            title=data["public_title"],
            description=data["description"],
            wordage=data["wordage"],
            published_at=normalize_datetime(data["first_shared_at"]),
            updated_at=normalize_datetime(data["last_updated_at"]),
            can_comment=data["commentable"],
            can_reprint=data["reprintable"],
            paid_info=ArticlePaidInfo(
                notebook_paid_status={
                    "free": None,  # 免费文章
                    "fbook_free": NotebookPaidStatusEnum.FREE,  # 免费连载中的免费文章
                    "pbook_free": NotebookPaidStatusEnum.PAID,  # 付费连载中的免费文章
                    "paid": None,  # 付费文章
                    "fbook_paid": NotebookPaidStatusEnum.FREE,  # 免费连载中的付费文章
                    "pbook_paid": NotebookPaidStatusEnum.PAID,  # 付费连载中的付费文章
                }[data["paid_type"]],
                article_paid_status={
                    "free": ArticlePaidStatusEnum.FREE,  # 免费文章
                    "fbook_free": ArticlePaidStatusEnum.FREE,  # 免费连载中的免费文章
                    "pbook_free": ArticlePaidStatusEnum.FREE,  # 付费连载中的免费文章
                    "paid": ArticlePaidStatusEnum.PAID,  # 付费文章
                    "fbook_paid": ArticlePaidStatusEnum.PAID,  # 免费连载中的付费文章
                    "pbook_paid": ArticlePaidStatusEnum.PAID,  # 付费连载中的付费文章
                }[data["paid_type"]],
                price=float(data["retail_price"]) / 100
                if data.get("retail_price")
                else None,
                paid_cotent_percent=float(data["paid_content_percent"].replace("%", ""))
                / 100
                if data.get("paid_content_percent")
                else None,
                paid_readers_count=data.get("purchased_count"),
            ),
            user_info=ArticleUserInfo(
                id=data["user"]["id"],
                slug=data["user"]["slug"],
                name=data["user"]["nickname"],
                avatar_url=data["user"]["avatar"],
                introduction=data["user"]["intro"],
                address_by_ip=data["user"]["user_ip_addr"],
                total_wordage=data["user"]["wordage"],
                total_likes_count=data["user"]["likes_count"],
            ),
            content=data["free_content"],
            likes_count=data["likes_count"],
            comments_count=data["public_comment_count"],
            featured_comments_count=data["featured_comments_count"],
            earned_fp_amount=normalize_assets_amount(data["total_fp_amount"]),
        )._validate()

    @property
    async def id(self) -> int:  # noqa: A003
        return (await self.info).id

    @property
    async def notebook_id(self) -> int:
        return (await self.info).notebook_id

    @property
    async def title(self) -> str:
        return (await self.info).title

    @property
    async def description(self) -> str:
        return (await self.info).description

    @property
    async def wordage(self) -> int:
        return (await self.info).wordage

    @property
    async def published_at(self) -> datetime:
        return (await self.info).published_at

    @property
    async def updated_at(self) -> datetime:
        return (await self.info).updated_at

    @property
    async def can_comment(self) -> bool:
        return (await self.info).can_comment

    @property
    async def can_reprint(self) -> bool:
        return (await self.info).can_reprint

    @property
    async def paid_info(self) -> ArticlePaidInfo:
        return (await self.info).paid_info

    @property
    async def user_info(self) -> ArticleUserInfo:
        return (await self.info).user_info

    @property
    async def content(self) -> str:
        return (await self.info).content

    @property
    async def views_count(self) -> int:
        await validate_if_necessary(self._validated, self.validate)

        data = await get_json(
            endpoint=ENDPOINT_CONFIG.jianshu,
            path=f"/shakespeare/v2/notes/{self.slug}/views_count",
        )

        return data["views_count"]

    @property
    async def likes_count(self) -> int:
        return (await self.info).likes_count

    @property
    async def comments_count(self) -> int:
        return (await self.info).comments_count

    @property
    async def featured_comments_count(self) -> int:
        return (await self.info).featured_comments_count

    @property
    async def earned_fp_amount(self) -> float:
        return (await self.info).earned_fp_amount
