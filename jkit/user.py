from datetime import datetime
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

from jkit._base import DATA_OBJECT_CONFIG, DataObject, StandardResourceObject
from jkit._constraints import (
    ArticleSlugStr,
    CollectionSlugStr,
    NonEmptyStr,
    NonNegativeFloat,
    NonNegativeInt,
    NormalizedDatetime,
    PositiveInt,
    UserNameStr,
    UserSlugStr,
    UserUploadedUrlStr,
)
from jkit._network_request import get_html, get_json
from jkit._normalization import normalize_assets_amount, normalize_datetime
from jkit._utils import check_if_necessary, only_one
from jkit.config import ENDPOINT_CONFIG
from jkit.exceptions import APIUnsupportedError, ResourceUnavailableError
from jkit.identifier_check import is_user_url
from jkit.identifier_convert import user_slug_to_url, user_url_to_slug

if TYPE_CHECKING:
    from jkit.article import Article
    from jkit.collection import Collection


class UserBadge(DataObject, **DATA_OBJECT_CONFIG):
    name: str
    introduction_url: str
    image_url: str


class MembershipEnum(Enum):
    NONE = "无会员"
    BRONZE = "铜牌会员"
    SLIVER = "银牌会员"
    GOLD = "金牌会员"
    PLATINA = "白金会员"


class GenderEnum(Enum):
    UNKNOWN = "未知"
    MALE = "男"
    FEMALE = "女"


class UserMembershipInfo(DataObject, **DATA_OBJECT_CONFIG):
    type: MembershipEnum  # noqa: A003
    expired_at: Optional[NormalizedDatetime]


class UserInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt  # noqa: A003
    name: UserNameStr
    gender: GenderEnum
    introduction: str
    introduction_updated_at: NormalizedDatetime
    avatar_url: UserUploadedUrlStr
    background_image_url: Optional[UserUploadedUrlStr]
    badges: Tuple[UserBadge, ...]
    membership_info: UserMembershipInfo
    address_by_ip: NonEmptyStr

    followers_count: NonNegativeInt
    fans_count: NonNegativeInt
    total_wordage: NonNegativeInt
    total_likes_count: NonNegativeInt
    fp_amount: NonNegativeFloat


class UserCollectionInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt  # noqa: A003
    slug: CollectionSlugStr
    name: NonEmptyStr
    image_url: UserUploadedUrlStr

    def get_collection_obj(self) -> "Collection":
        from jkit.collection import Collection

        return Collection.from_slug(self.slug)._from_trusted_source()


class UserNotebookInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt  # noqa: A003
    name: NonEmptyStr
    is_book: bool  # TODO: 命名修改
    is_paid_book: Optional[bool]  # TODO: 命名修改

    # TODO: get_notebook_obj


class UserArticleAuthorInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt  # noqa: A003
    slug: UserSlugStr
    name: UserNameStr
    avatar_url: UserUploadedUrlStr

    def to_user_obj(self) -> "User":
        from jkit.user import User

        return User.from_slug(self.slug)._from_trusted_source()


class UserArticleInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt  # noqa: A003
    slug: ArticleSlugStr
    title: NonEmptyStr
    description: str
    image_url: Optional[UserUploadedUrlStr]
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

        return Article.from_slug(self.slug)._from_trusted_source()


class User(StandardResourceObject):
    def __init__(
        self, *, url: Optional[str] = None, slug: Optional[str] = None
    ) -> None:
        super().__init__()

        if not only_one(url, slug):
            raise ValueError("url 和 slug 不可同时提供")

        if url:
            if not is_user_url(url):
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

    async def check(self) -> None:
        if self._checked:
            return

        try:
            await get_json(
                endpoint=ENDPOINT_CONFIG.jianshu,
                path=f"/asimov/users/slug/{self.slug}",
            )
        except HTTPStatusError:
            raise ResourceUnavailableError(
                f"用户 {self.url} 不存在或已注销 / 被封禁"
            ) from None

    @property
    async def info(self) -> UserInfo:
        await check_if_necessary(self._checked, self.check)

        data = await get_json(
            endpoint=ENDPOINT_CONFIG.jianshu,
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
                    "sliver": MembershipEnum.SLIVER,
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
    async def background_image_url(self) -> Optional[str]:
        return (await self.info).background_image_url

    @property
    async def badges(self) -> Tuple[UserBadge, ...]:
        return (await self.info).badges

    @property
    async def membership(self) -> UserMembershipInfo:
        return (await self.info).membership_info

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

    @property
    async def fp_amount(self) -> float:
        return (await self.info).fp_amount

    @property
    async def assets_amount(self) -> float:
        data = await get_html(endpoint=ENDPOINT_CONFIG.jianshu, path=f"/u/{self.slug}")

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

    @property
    async def ftn_amount(self) -> float:
        return round((await self.assets_amount) - (await self.fp_amount), 3)

    async def owned_collections(
        self, page: int = 1, page_size: int = 10
    ) -> Tuple[UserCollectionInfo, ...]:
        data = await get_json(
            endpoint=ENDPOINT_CONFIG.jianshu,
            path=f"/users/{self.slug}/collections",
            params={
                "slug": self.slug,
                "type": "own",
                "page": page,
                "per_page": page_size,
            },
        )

        return tuple(
            UserCollectionInfo(
                id=item["id"],
                slug=item["slug"],
                name=item["title"],
                image_url=item["avatar"],
            )._validate()
            for item in data["collections"]
        )

    async def managed_collections(
        self, page: int = 1, page_size: int = 10
    ) -> Tuple[UserCollectionInfo, ...]:
        data = await get_json(
            endpoint=ENDPOINT_CONFIG.jianshu,
            path=f"/users/{self.slug}/collections",
            params={
                "slug": self.slug,
                "type": "manager",
                "page": page,
                "per_page": page_size,
            },
        )

        return tuple(
            UserCollectionInfo(
                id=item["id"],
                slug=item["slug"],
                name=item["title"],
                image_url=item["avatar"],
            )._validate()
            for item in data["collections"]
        )

    async def notebooks(
        self, page: int = 1, page_size: int = 10
    ) -> Tuple[UserNotebookInfo, ...]:
        data = await get_json(
            endpoint=ENDPOINT_CONFIG.jianshu,
            path=f"/users/{self.slug}/notebooks",
            params={
                "slug": self.slug,
                "type": "manager",
                "page": page,
                "per_page": page_size,
            },
        )

        return tuple(
            UserNotebookInfo(
                id=item["id"],
                name=item["name"],
                is_book=item["book"],
                is_paid_book=item.get("paid_book"),
            )._validate()
            for item in data["notebooks"]
        )

    async def iter_articles(
        self,
        *,
        start_page: int = 1,
        order_by: Literal[
            "published_at", "last_comment_time", "popularity"
        ] = "published_at",
        page_size: int = 10,
    ) -> AsyncGenerator[UserArticleInfo, None]:
        now_page = start_page
        while True:
            data: List[Dict[str, Any]] = await get_json(
                endpoint=ENDPOINT_CONFIG.jianshu,
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
