from datetime import datetime
from enum import Enum
from typing import Annotated, Optional, Tuple

from msgspec import Meta

from jkit.constants import UPLOAD_JIANSHU_IO_URL_REGEX, USER_SLUG_REGEX, USER_URL_REGEX
from jkit.data_objects._base import DATA_OBJECT_CONFIG, DataObject


class UserBadge(DataObject, **DATA_OBJECT_CONFIG):
    name: str
    introduction_url: str
    image_url: str


class MembershipEnum(Enum):
    NONE = "none"
    BRONZE = "bronze"
    SLIVER = "sliver"
    GOLD = "gold"
    PLATINA = "platina"


class GenderEnum(Enum):
    UNKNOWN = "unknown"
    MALE = "male"
    FEMALE = "female"


class UserMembership(DataObject, **DATA_OBJECT_CONFIG):
    type: MembershipEnum  # noqa: A003
    expired_at: Optional[datetime]


class UserInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: Annotated[int, Meta(gt=0)]  # noqa: A003
    url: Annotated[str, Meta(pattern=USER_URL_REGEX.pattern)]
    slug: Annotated[str, Meta(pattern=USER_SLUG_REGEX.pattern)]
    name: str
    gender: GenderEnum
    introduction: str
    introduction_updated_at: datetime
    avatar_url: Annotated[str, Meta(pattern=UPLOAD_JIANSHU_IO_URL_REGEX.pattern)]
    background_image_url: Annotated[
        str, Meta(pattern=UPLOAD_JIANSHU_IO_URL_REGEX.pattern)
    ]
    badges: Tuple[UserBadge, ...]
    membership: UserMembership
    address_by_ip: Annotated[str, Meta(min_length=1)]

    followers_count: Annotated[int, Meta(ge=0)]
    fans_count: Annotated[int, Meta(ge=0)]
    total_wordage: Annotated[int, Meta(ge=0)]
    total_likes_count: Annotated[int, Meta(ge=0)]
    # TODO: 简书钻数量
