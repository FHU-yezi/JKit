from typing import TYPE_CHECKING, Any, AsyncGenerator, Dict, List

from jkit._base import DATA_OBJECT_CONFIG, DataObject, ResourceObject
from jkit._constraints import (
    NonEmptyStr,
    NormalizedDatetime,
    PositiveInt,
    UserName,
    UserSlug,
    UserUploadedUrl,
)
from jkit._network_request import get_json
from jkit._normalization import normalize_datetime
from jkit.config import CONFIG

if TYPE_CHECKING:
    from jkit.user import User


class UserInfoField(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt
    slug: UserSlug
    name: UserName
    avatar_url: UserUploadedUrl

    def to_user_obj(self) -> "User":
        from jkit.user import User

        return User.from_slug(self.slug)._as_checked()


class JianshuLotteryWinRecord(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt
    time: NormalizedDatetime
    award_name: NonEmptyStr

    user_info: UserInfoField


class JianshuLottery(ResourceObject):
    async def iter_win_records(
        self, *, count: int = 100
    ) -> AsyncGenerator[JianshuLotteryWinRecord, None]:
        data: List[Dict[str, Any]] = await get_json(
            endpoint=CONFIG.endpoints.jianshu,
            path="/asimov/ad_rewards/winner_list",
            params={"count": count},
        )  # type: ignore

        for item in data:
            yield JianshuLotteryWinRecord(
                id=item["id"],
                time=normalize_datetime(item["created_at"]),
                award_name=item["name"],
                user_info=UserInfoField(
                    id=item["user"]["id"],
                    slug=item["user"]["slug"],
                    name=item["user"]["nickname"],
                    avatar_url=item["user"]["avatar"],
                ),
            )._validate()
