from enum import Enum
from typing import Optional, Tuple

from jkit._constraints import (
    NonEmptyStr,
    NonNegativeInt,
    NormalizedDatetime,
    PositiveInt,
    UploadJianshuIoUrlStr,
    UserNameStr,
    UserSlugStr,
    UserUrlStr,
)
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
    expired_at: Optional[NormalizedDatetime]


class UserInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt  # noqa: A003
    url: UserUrlStr
    slug: UserSlugStr
    name: UserNameStr
    gender: GenderEnum
    introduction: str
    introduction_updated_at: NormalizedDatetime
    avatar_url: UploadJianshuIoUrlStr
    background_image_url: UploadJianshuIoUrlStr
    badges: Tuple[UserBadge, ...]
    membership: UserMembership
    address_by_ip: NonEmptyStr

    followers_count: NonNegativeInt
    fans_count: NonNegativeInt
    total_wordage: NonNegativeInt
    total_likes_count: NonNegativeInt
    # TODO: 简书钻数量
