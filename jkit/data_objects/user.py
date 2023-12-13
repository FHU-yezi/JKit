from datetime import datetime
from enum import Enum
from typing import Annotated, Optional, Tuple

from msgspec import Meta

from jkit.data_objects._base import DATA_OBJECT_CONFIG, DataObject


class UserBadge(DataObject, **DATA_OBJECT_CONFIG):
    name: str
    introduction_url: str
    image_url: str


class MembershipEnum(Enum):
    NO_MEMBERSHIP = None
    BRONZE = "bronze"
    SLIVER = "sliver"
    gold = "gold"
    PLATINA = "platina"


class GenderEnum(Enum):
    UNKNOWN = None
    MALE = "male"
    FEMALE = "female"

class UserMembership(DataObject, **DATA_OBJECT_CONFIG):
    type: MembershipEnum  # noqa: A003
    expired_at: Optional[datetime]


class UserInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: Annotated[int, Meta(gt=0)]  # noqa: A003
    url: str
    slug: str
    name: str
    gender: GenderEnum
    introduction: str
    introduction_updated_at: datetime
    avatar_url: str
    background_image_url: str
    badges: Tuple[UserBadge, ...]
    membership: UserMembership
    address_by_ip: str

    followers_count: Annotated[int, Meta(ge=0)]
    fans_count: Annotated[int, Meta(ge=0)]
    total_wordage: Annotated[int, Meta(ge=0)]
    total_likes_count: Annotated[int, Meta(ge=0)]
    # TODO: 简书钻数量
