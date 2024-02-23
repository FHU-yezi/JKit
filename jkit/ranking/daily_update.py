from typing import TYPE_CHECKING, AsyncGenerator

from jkit._base import DATA_OBJECT_CONFIG, DataObject, ResourceObject
from jkit._constraints import PositiveInt, UserName, UserSlug, UserUploadedUrl
from jkit._network_request import get_json
from jkit.config import CONFIG

if TYPE_CHECKING:
    from jkit.user import User


class DailyUpdateRankingRecordUserInfo(DataObject, **DATA_OBJECT_CONFIG):
    slug: UserSlug
    name: UserName
    avatar_url: UserUploadedUrl

    def to_user_obj(self) -> "User":
        from jkit.user import User

        return User.from_slug(self.slug)._as_checked()


class DailyUpdateRankingRecord(DataObject, **DATA_OBJECT_CONFIG):
    ranking: PositiveInt
    days: PositiveInt
    user_info: DailyUpdateRankingRecordUserInfo


class DailyUpdateRanking(ResourceObject):
    async def __aiter__(self) -> AsyncGenerator[DailyUpdateRankingRecord, None]:
        data = await get_json(
            endpoint=CONFIG.endpoints.jianshu,
            path="/asimov/daily_activity_participants/rank",
        )

        for item in data["daps"]:
            yield DailyUpdateRankingRecord(
                ranking=item["rank"],
                days=item["checkin_count"],
                user_info=DailyUpdateRankingRecordUserInfo(
                    slug=item["slug"],
                    name=item["nickname"],
                    avatar_url=item["avatar"],
                ),
            )._validate()
