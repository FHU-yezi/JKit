from datetime import datetime
from enum import Enum
from re import sub as re_sub
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncGenerator,
    Dict,
    List,
    Literal,
    Optional,
    Tuple,
)

from httpx import HTTPStatusError
from lxml.html import HtmlElement
from lxml.html import fromstring as parse_html
from typing_extensions import Self

from jkit._base import (
    DATA_OBJECT_CONFIG,
    CheckableObject,
    DataObject,
    ResourceObject,
    SlugAndUrlObject,
)
from jkit._constraints import (
    CollectionSlug,
    NonEmptyStr,
    NonNegativeFloat,
    NonNegativeInt,
    NormalizedDatetime,
    Percentage,
    PositiveFloat,
    PositiveInt,
    UserName,
    UserSlug,
    UserUploadedUrl,
)
from jkit._network_request import get_json
from jkit._normalization import (
    normalize_assets_amount,
    normalize_datetime,
    normalize_percentage,
)
from jkit._utils import only_one
from jkit.config import ENDPOINT_CONFIG
from jkit.exceptions import ResourceUnavailableError
from jkit.identifier_check import is_article_url
from jkit.identifier_convert import article_slug_to_url, article_url_to_slug

if TYPE_CHECKING:
    from jkit.collection import Collection
    from jkit.notebook import Notebook
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


class ArticleAuthorInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt
    slug: UserSlug
    name: UserName
    avatar_url: UserUploadedUrl
    introduction: str
    address_by_ip: NonEmptyStr

    total_wordage: NonNegativeInt
    total_likes_count: NonNegativeInt

    def to_user_obj(self) -> "User":
        from jkit.user import User

        return User.from_slug(self.slug)._as_checked()


class ArticleInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt
    notebook_id: PositiveInt
    title: NonEmptyStr
    description: NonEmptyStr
    wordage: PositiveInt
    published_at: NormalizedDatetime
    updated_at: NormalizedDatetime
    can_comment: bool
    can_reprint: bool
    paid_info: ArticlePaidInfo
    author_info: ArticleAuthorInfo
    html_content: NonEmptyStr

    likes_count: NonNegativeInt
    comments_count: NonNegativeInt
    featured_comments_count: NonNegativeInt
    earned_fp_amount: NonNegativeFloat

    @property
    def text_content(self) -> str:
        html_obj: HtmlElement = parse_html(self.html_content)
        result = "".join(html_obj.itertext())  # type: ignore
        return re_sub(r"\s{3,}", "", result)  # 去除多余的空行


class ArticleAudioInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt
    name: NonEmptyStr
    producer: NonEmptyStr
    file_url: str  # TODO
    duration_seconds: PositiveInt
    file_size_bytes: PositiveInt

    @property
    def file_url_expire_time(self) -> datetime:
        return datetime.fromtimestamp(
            int(self.file_url.split("?")[1].split("&")[0].replace("Expires=", ""))
        )

    @property
    def is_file_expired(self) -> bool:
        return self.file_url_expire_time >= datetime.now()


class ArticleIncludedCollectionInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt
    slug: CollectionSlug
    name: NonEmptyStr
    image_url: UserUploadedUrl
    owner_name: UserName

    def to_collection_obj(self) -> "Collection":
        from jkit.collection import Collection

        return Collection.from_slug(self.slug)._as_checked()

    @property
    async def full_name(self) -> str:
        if "..." not in self.name:
            return self.name

        return (await self.to_collection_obj().info).name


class ArticleBelongToNotebookInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt
    name: NonEmptyStr

    def to_notebook_obj(self) -> "Notebook":
        from jkit.notebook import Notebook

        return Notebook.from_id(self.id)


class ArticleCommentPublisherInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt
    slug: UserSlug
    name: UserName
    avatar_url: UserUploadedUrl
    address_by_ip: NonEmptyStr

    @property
    def to_user_obj(self) -> "User":
        from jkit.user import User

        return User.from_slug(self.slug)._as_checked()


class ArticleSubcommentInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt
    content: str
    images: Tuple[UserUploadedUrl, ...]
    published_at: NormalizedDatetime
    publisher_info: ArticleCommentPublisherInfo


class ArticleCommentInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt
    floor: PositiveInt
    content: str
    images: Tuple[UserUploadedUrl, ...]
    likes_count: NonNegativeInt
    published_at: NormalizedDatetime
    publisher_info: ArticleCommentPublisherInfo

    subcomments: Tuple[ArticleSubcommentInfo, ...]

    @property
    def has_subcomment(self) -> bool:
        return bool(self.subcomments)


class ArticleFeaturedCommentInfo(ArticleCommentInfo, **DATA_OBJECT_CONFIG):
    score: PositiveInt


class Article(ResourceObject, CheckableObject, SlugAndUrlObject):
    def __init__(
        self, *, url: Optional[str] = None, slug: Optional[str] = None
    ) -> None:
        super().__init__()

        if not only_one(url, slug):
            raise ValueError("文章链接和文章 Slug 不可同时提供")

        if url:
            if not is_article_url(url):
                raise ValueError(f"{url} 不是有效的文章链接")
            self._url = url
        elif slug:
            self._url = article_slug_to_url(slug)
        else:
            raise ValueError("必须提供文章链接或文章 Slug")

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

    async def check(self) -> None:
        if self._checked:
            return

        try:
            await get_json(
                endpoint=ENDPOINT_CONFIG.jianshu,
                path=f"/asimov/p/{self.slug}",
            )
            self._checked = True
        except HTTPStatusError:
            raise ResourceUnavailableError(
                f"文章 {self.url} 不存在或已被锁定 / 私密 / 删除"
            ) from None

    @property
    async def id(self) -> int:
        return (await self.info).id

    @property
    async def info(self) -> ArticleInfo:
        await self._auto_check()

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
                paid_cotent_percent=normalize_percentage(
                    float(data["paid_content_percent"].replace("%", ""))
                )
                if data.get("paid_content_percent")
                else None,
                paid_readers_count=data.get("purchased_count"),
            ),
            author_info=ArticleAuthorInfo(
                id=data["user"]["id"],
                slug=data["user"]["slug"],
                name=data["user"]["nickname"],
                avatar_url=data["user"]["avatar"],
                introduction=data["user"]["intro"],
                address_by_ip=data["user"]["user_ip_addr"],
                total_wordage=data["user"]["wordage"],
                total_likes_count=data["user"]["likes_count"],
            ),
            html_content=data["free_content"],
            likes_count=data["likes_count"],
            comments_count=data["public_comment_count"],
            featured_comments_count=data["featured_comments_count"],
            earned_fp_amount=normalize_assets_amount(data["total_fp_amount"]),
        )._validate()

    @property
    async def views_count(self) -> int:
        await self._auto_check()

        data = await get_json(
            endpoint=ENDPOINT_CONFIG.jianshu,
            path=f"/shakespeare/v2/notes/{self.slug}/views_count",
        )

        return data["views_count"]

    @property
    async def audio_info(self) -> Optional[ArticleAudioInfo]:
        await self._auto_check()

        data = await get_json(
            endpoint=ENDPOINT_CONFIG.jianshu,
            path=f"/shakespeare/v2/notes/{self.slug}/audio",
        )

        if not data["exists"]:
            return None

        return ArticleAudioInfo(
            id=data["id"],
            name=data["title"],
            producer=data["dubber"],
            file_url=data["play_url"],
            duration_seconds=data["duration"],
            file_size_bytes=data["filesize"],
        )._validate()

    @property
    async def belong_to_notebook(self) -> ArticleBelongToNotebookInfo:
        await self._auto_check()

        data = await get_json(
            endpoint=ENDPOINT_CONFIG.jianshu,
            path=f"/shakespeare/v2/notes/{self.slug}/book",
        )

        return ArticleBelongToNotebookInfo(
            id=data["notebook_id"],
            name=data["notebook_name"],
        )._validate()

    async def iter_included_collections(
        self, *, start_page: int = 1, page_size: int = 10
    ) -> AsyncGenerator[ArticleIncludedCollectionInfo, None]:
        await self._auto_check()

        now_page = start_page
        while True:
            data = await get_json(
                endpoint=ENDPOINT_CONFIG.jianshu,
                path=f"/shakespeare/notes/{await self.id}/included_collections",
                params={"page": now_page, "count": page_size},
            )
            if not data["collections"]:
                return

            for item in data["collections"]:
                yield ArticleIncludedCollectionInfo(
                    id=item["id"],
                    slug=item["slug"],
                    name=item["title"],
                    image_url=item["avatar"],
                    owner_name=item["owner_name"],
                )._validate()

            now_page += 1

    async def iter_comments(
        self,
        *,
        start_page: int = 1,
        direction: Literal["asc", "desc"] = "desc",
        author_only: bool = False,
        page_size: int = 10,
    ) -> AsyncGenerator[ArticleCommentInfo, None]:
        await self._auto_check()

        now_page = start_page
        while True:
            data = await get_json(
                endpoint=ENDPOINT_CONFIG.jianshu,
                path=f"/shakespeare/notes/{await self.id}/comments",
                params={
                    "page": now_page,
                    "order_by": direction,
                    "author_only": author_only,
                    "count": page_size,
                },
            )
            if not data["comments"]:
                return

            for item in data["comments"]:
                yield ArticleCommentInfo(
                    id=item["id"],
                    floor=item["floor"],
                    content=item["compiled_content"],
                    images=tuple(image["url"] for image in item["images"])
                    if item["images"]
                    else (),
                    likes_count=item["likes_count"],
                    published_at=normalize_datetime(item["created_at"]),
                    publisher_info=ArticleCommentPublisherInfo(
                        id=item["user"]["id"],
                        slug=item["user"]["slug"],
                        name=item["user"]["nickname"],
                        avatar_url=item["user"]["avatar"],
                        address_by_ip=item["user"]["user_ip_addr"],
                    ),
                    subcomments=tuple(
                        ArticleSubcommentInfo(
                            id=subcomment["id"],
                            content=subcomment["compiled_content"],
                            images=tuple(image["url"] for image in subcomment["images"])
                            if subcomment["images"]
                            else (),
                            published_at=normalize_datetime(subcomment["created_at"]),
                            publisher_info=ArticleCommentPublisherInfo(
                                id=subcomment["user"]["id"],
                                slug=subcomment["user"]["slug"],
                                name=subcomment["user"]["nickname"],
                                avatar_url=subcomment["user"]["avatar"],
                                address_by_ip=subcomment["user"]["user_ip_addr"],
                            ),
                        )
                        for subcomment in item["children"]
                    ),
                )._validate()

            now_page += 1

    async def iter_featured_comments(
        self,
        *,
        count: int = 10,
    ) -> AsyncGenerator[ArticleFeaturedCommentInfo, None]:
        await self._auto_check()

        data: List[Dict[str, Any]] = await get_json(
            endpoint=ENDPOINT_CONFIG.jianshu,
            path=f"/shakespeare/notes/{self.slug}/featured_comments",
            params={
                "count": count,
            },
        )  # type: ignore

        for item in data:
            yield ArticleFeaturedCommentInfo(
                id=item["id"],
                floor=item["floor"],
                content=item["compiled_content"],
                images=tuple(image["url"] for image in item["images"])
                if item["images"]
                else (),
                likes_count=item["likes_count"],
                published_at=normalize_datetime(item["created_at"]),
                publisher_info=ArticleCommentPublisherInfo(
                    id=item["user"]["id"],
                    slug=item["user"]["slug"],
                    name=item["user"]["nickname"],
                    avatar_url=item["user"]["avatar"],
                    address_by_ip=item["user"]["user_ip_addr"],
                ),
                subcomments=tuple(
                    ArticleSubcommentInfo(
                        id=subcomment["id"],
                        content=subcomment["compiled_content"],
                        images=tuple(image["url"] for image in subcomment["images"])
                        if subcomment["images"]
                        else (),
                        published_at=normalize_datetime(subcomment["created_at"]),
                        publisher_info=ArticleCommentPublisherInfo(
                            id=subcomment["user"]["id"],
                            slug=subcomment["user"]["slug"],
                            name=subcomment["user"]["nickname"],
                            avatar_url=subcomment["user"]["avatar"],
                            address_by_ip=subcomment["user"]["user_ip_addr"],
                        ),
                    )
                    for subcomment in item["children"]
                ),
                score=item["score"],
            )._validate()
