from enum import Enum
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
from typing_extensions import Self

from jkit._base import (
    DATA_OBJECT_CONFIG,
    CheckableObject,
    DataObject,
    ResourceObject,
    SlugAndUrlObject,
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
from jkit._network_request import get_html, get_json
from jkit._normalization import normalize_assets_amount, normalize_datetime
from jkit._utils import only_one
from jkit.config import CONFIG
from jkit.exceptions import APIUnsupportedError, ResourceUnavailableError
from jkit.identifier_check import is_user_url
from jkit.identifier_convert import user_slug_to_url, user_url_to_slug

if TYPE_CHECKING:
    from jkit.article import Article
    from jkit.collection import Collection
    from jkit.notebook import Notebook


class UserBadge(DataObject, **DATA_OBJECT_CONFIG):
    name: NonEmptyStr
    introduction_url: str
    image_url: NonEmptyStr


class MembershipEnum(Enum):
    NONE = "无会员"
    BRONZE = "铜牌会员"
    SILVER = "银牌会员"
    GOLD = "金牌会员"
    PLATINA = "白金会员"


class GenderEnum(Enum):
    UNKNOWN = "未知"
    MALE = "男"
    FEMALE = "女"


class UserMembershipInfo(DataObject, **DATA_OBJECT_CONFIG):
    type: MembershipEnum
    expired_at: Optional[NormalizedDatetime]


class UserInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt
    name: UserName
    gender: GenderEnum
    introduction: str
    introduction_updated_at: NormalizedDatetime
    avatar_url: UserUploadedUrl
    background_image_url: Optional[UserUploadedUrl]
    badges: Tuple[UserBadge, ...]
    membership_info: UserMembershipInfo
    address_by_ip: NonEmptyStr

    followers_count: NonNegativeInt
    fans_count: NonNegativeInt
    total_wordage: NonNegativeInt
    total_likes_count: NonNegativeInt
    fp_amount: NonNegativeFloat


class UserCollectionInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt
    slug: CollectionSlug
    name: NonEmptyStr
    image_url: UserUploadedUrl

    def to_collection_obj(self) -> "Collection":
        from jkit.collection import Collection

        return Collection.from_slug(self.slug)._as_checked()


class UserNotebookInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt
    name: NonEmptyStr
    is_serial: bool
    is_paid: Optional[bool]

    def to_notebook_obj(self) -> "Notebook":
        from jkit.notebook import Notebook

        return Notebook.from_id(self.id)


class UserArticleAuthorInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt
    slug: UserSlug
    name: UserName
    avatar_url: UserUploadedUrl

    def to_user_obj(self) -> "User":
        from jkit.user import User

        return User.from_slug(self.slug)._as_checked()


class UserArticleInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt
    slug: ArticleSlug
    title: NonEmptyStr
    description: str
    image_url: Optional[UserUploadedUrl]
    published_at: NormalizedDatetime
    is_top: bool
    is_paid: bool
    can_comment: bool
    author_info: UserArticleAuthorInfo

    views_count: NonNegativeInt
    likes_count: NonNegativeInt
    comments_count: NonNegativeInt
    tips_count: NonNegativeInt
    earned_fp_amount: NonNegativeFloat

    def to_article_obj(self) -> "Article":
        from jkit.article import Article

        return Article.from_slug(self.slug)._as_checked()


class User(ResourceObject, CheckableObject, SlugAndUrlObject):
    def __init__(
        self, *, url: Optional[str] = None, slug: Optional[str] = None
    ) -> None:
        super().__init__()

        if not only_one(url, slug):
            raise ValueError("用户链接与用户 Slug 不可同时提供")

        if url:
            if not is_user_url(url):
                raise ValueError(f"{url} 不是有效的用户链接")
            self._url = url
        elif slug:
            self._url = user_slug_to_url(slug)
        else:
            raise ValueError("必须提供用户链接或用户 Slug")

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

    async def check(self) -> None:
        if self._checked:
            return

        try:
            await get_json(
                endpoint=CONFIG.endpoints.jianshu,
                path=f"/asimov/users/slug/{self.slug}",
            )
        except HTTPStatusError:
            raise ResourceUnavailableError(
                f"用户 {self.url} 不存在或已注销 / 被封禁"
            ) from None

    @property
    async def id(self) -> int:
        return (await self.info).id

    @property
    async def info(self) -> UserInfo:
        await self._auto_check()

        data = await get_json(
            endpoint=CONFIG.endpoints.jianshu,
            path=f"/asimov/users/slug/{self.slug}",
        )

        return UserInfo(
            id=data["id"],
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
            background_image_url=data["background_image"]
            if data.get("background_image")
            else None,
            badges=tuple(
                UserBadge(
                    name=badge["text"],
                    introduction_url=badge["intro_url"],
                    image_url=badge["image_url"],
                )
                for badge in data["badges"]
            ),
            membership_info=UserMembershipInfo(
                type={
                    "bronze": MembershipEnum.BRONZE,
                    "silver": MembershipEnum.SILVER,
                    "gold": MembershipEnum.GOLD,
                    "platina": MembershipEnum.PLATINA,
                }[data["member"]["type"]],
                expired_at=normalize_datetime(data["member"]["expires_at"]),
            )
            if data.get("member")
            else UserMembershipInfo(
                type=MembershipEnum.NONE,
                expired_at=None,
            ),
            address_by_ip=data["user_ip_addr"],
            followers_count=data["following_users_count"],
            fans_count=data["followers_count"],
            total_wordage=data["total_wordage"],
            total_likes_count=data["total_likes_count"],
            fp_amount=normalize_assets_amount(data["jsd_balance"]),
        )._validate()

    @property
    async def fp_amount(self) -> float:
        return (await self.info).fp_amount

    @property
    async def ftn_amount(self) -> float:
        return round((await self.assets_amount) - (await self.info).fp_amount, 3)

    @property
    async def assets_amount(self) -> float:
        await self._auto_check()

        data = await get_html(endpoint=CONFIG.endpoints.jianshu, path=f"/u/{self.slug}")

        try:
            return float(
                data.xpath("//div[@class='meta-block']/p")[2]
                .text.replace(".", "")
                .replace("w", "000")
            )
        except IndexError:
            raise APIUnsupportedError(
                "受 API 限制，无法获取此用户的资产量信息"
            ) from None

    async def iter_owned_collections(
        self, *, start_page: int = 1, page_size: int = 10
    ) -> AsyncGenerator[UserCollectionInfo, None]:
        await self._auto_check()

        now_page = start_page
        while True:
            data = await get_json(
                endpoint=CONFIG.endpoints.jianshu,
                path=f"/users/{self.slug}/collections",
                params={
                    "slug": self.slug,
                    "type": "own",
                    "page": now_page,
                    "per_page": page_size,
                },
            )
            if not data["collections"]:
                return

            for item in data["collections"]:
                yield UserCollectionInfo(
                    id=item["id"],
                    slug=item["slug"],
                    name=item["title"],
                    image_url=item["avatar"],
                )._validate()

            now_page += 1

    async def iter_managed_collections(
        self, *, start_page: int = 1, page_size: int = 10
    ) -> AsyncGenerator[UserCollectionInfo, None]:
        await self._auto_check()

        now_page = start_page
        while True:
            data = await get_json(
                endpoint=CONFIG.endpoints.jianshu,
                path=f"/users/{self.slug}/collections",
                params={
                    "slug": self.slug,
                    "type": "manager",
                    "page": now_page,
                    "per_page": page_size,
                },
            )
            if not data["collections"]:
                return

            for item in data["collections"]:
                yield UserCollectionInfo(
                    id=item["id"],
                    slug=item["slug"],
                    name=item["title"],
                    image_url=item["avatar"],
                )._validate()

            now_page += 1

    async def iter_notebooks(
        self, *, start_page: int = 1, page_size: int = 10
    ) -> AsyncGenerator[UserNotebookInfo, None]:
        await self._auto_check()

        now_page = start_page
        while True:
            data = await get_json(
                endpoint=CONFIG.endpoints.jianshu,
                path=f"/users/{self.slug}/notebooks",
                params={
                    "slug": self.slug,
                    "type": "manager",
                    "page": now_page,
                    "per_page": page_size,
                },
            )
            if not data["notebooks"]:
                return

            for item in data["notebooks"]:
                yield UserNotebookInfo(
                    id=item["id"],
                    name=item["name"],
                    is_serial=item["book"],
                    is_paid=item.get("paid_book"),
                )._validate()

            now_page += 1

    async def iter_articles(
        self,
        *,
        start_page: int = 1,
        order_by: Literal[
            "published_at", "last_comment_time", "popularity"
        ] = "published_at",
        page_size: int = 10,
    ) -> AsyncGenerator[UserArticleInfo, None]:
        await self._auto_check()

        now_page = start_page
        while True:
            data: List[Dict[str, Any]] = await get_json(
                endpoint=CONFIG.endpoints.jianshu,
                path=f"/asimov/users/slug/{self.slug}/public_notes",
                params={
                    "page": now_page,
                    "count": page_size,
                    "order_by": {
                        "published_at": "shared_at",
                        "last_comment_time": "commented_at",
                        "popularity": "top",
                    }[order_by],
                },
            )  # type: ignore
            if not data:
                return

            for item in data:
                yield UserArticleInfo(
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
                    is_top=item["object"]["data"]["is_top"],
                    is_paid=item["object"]["data"]["paid"],
                    can_comment=item["object"]["data"]["commentable"],
                    author_info=UserArticleAuthorInfo(
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
