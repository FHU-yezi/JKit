from enum import Enum
from typing import Optional

from typing_extensions import Self

from jkit._base import DATA_OBJECT_CONFIG, DataObject, ResourceObject
from jkit._constraints import (
    NonEmptyStr,
    NonNegativeFloat,
    NonNegativeInt,
    NormalizedDatetime,
    Percentage,
    PositiveFloat,
    PositiveInt,
)
from jkit._http_client import get_json
from jkit._normalization import normalize_datetime
from jkit._utils import only_one
from jkit.config import ENDPOINT_CONFIG
from jkit.identifier_assert import assert_article_url
from jkit.identifier_convert import article_slug_to_url, article_url_to_slug


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
    content: NonEmptyStr

    likes_count: NonNegativeInt
    comments_count: NonNegativeInt
    featured_comments_count: NonNegativeInt
    earned_fp_amount: NonNegativeFloat


# TODO: 文章状态校验
class Article(ResourceObject):
    def __init__(
        self, *, url: Optional[str] = None, slug: Optional[str] = None
    ) -> None:
        if not only_one(url, slug):
            raise ValueError("url 和 slug 不可同时提供")

        if url:
            if not assert_article_url(url):
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

    @property
    async def info(self) -> ArticleInfo:
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
            content=data["free_content"],
            likes_count=data["likes_count"],
            comments_count=data["public_comment_count"],
            featured_comments_count=data["featured_comments_count"],
            earned_fp_amount=data["total_fp_amount"] / 1000,
        ).validate()

    @property
    async def id(self) -> int:  # noqa: A003
        return (await self.info).id

    @property
    async def title(self) -> str:
        return (await self.info).title

    @property
    async def content(self) -> str:
        return (await self.info).content
