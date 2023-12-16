from datetime import date, datetime
from typing import TYPE_CHECKING, Literal, Tuple

from jkit._base import DATA_OBJECT_CONFIG, DataObject, ResourceObject
from jkit._constraints import (
    PositiveFloat,
    UserNameStr,
    UserSlugStr,
    UserUploadedUrlStr,
)
from jkit._http_client import get_json
from jkit.config import ENDPOINT_CONFIG
from jkit.exceptions import APIUnsupportedError

if TYPE_CHECKING:
    from jkit.user import User


class UserEarningRankRecord(DataObject, **DATA_OBJECT_CONFIG):
    name: UserNameStr
    slug: UserSlugStr
    avatar_url: UserUploadedUrlStr
    total_fp_amount: PositiveFloat
    fp_by_creating_anount: PositiveFloat
    fp_by_voting_amount: PositiveFloat

    def get_user_obj(self) -> "User":
        from jkit.user import User

        return User.from_slug(self.slug)


class UserEarningRankData(DataObject, **DATA_OBJECT_CONFIG):
    total_fp_amount_sum: PositiveFloat
    fp_by_creating_amount_sum: PositiveFloat
    fp_by_voting_amount_sum: PositiveFloat
    records: Tuple[UserEarningRankRecord, ...]


class UserEarningRank(ResourceObject):
    def __init__(
        self,
        target_date: date,
        /,
        *,
        type: Literal["all", "creating", "voting"] = "all",  # noqa: A002
    ) -> None:
        if target_date < date(2020, 6, 20):
            raise APIUnsupportedError("仅支持获取 2020.06.20 后的排行榜数据")
        if target_date >= datetime.now().date():
            raise ValueError("不支持获取尚未生成的排行榜数据")

        self._target_date = target_date
        self._type = type

    async def get_data(self) -> UserEarningRankData:
        data = await get_json(
            endpoint=ENDPOINT_CONFIG.jianshu,
            path="/asimov/fp_rankings/voter_users",
            params={
                "type": {"all": None, "creating": "note", "voting": "like"}[self._type],
                "date": self._target_date.strftime(r"%Y%m%d"),
            },
        )

        return UserEarningRankData(
            total_fp_amount_sum=data["fp"] / 1000,
            fp_by_creating_amount_sum=data["author_fp"] / 1000,
            fp_by_voting_amount_sum=data["voter_fp"] / 1000,
            records=tuple(
                UserEarningRankRecord(
                    name=item["nickname"],
                    slug=item["slug"],
                    avatar_url=item["avatar"],
                    total_fp_amount=item["fp"] / 1000,
                    fp_by_creating_anount=item["author_fp"] / 1000,
                    fp_by_voting_amount=item["voter_fp"] / 1000,
                )
                for item in data["users"]
            ),
        )
