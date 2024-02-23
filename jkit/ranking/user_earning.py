from datetime import date, datetime
from typing import TYPE_CHECKING, AsyncGenerator, Literal, Tuple

from jkit._base import DATA_OBJECT_CONFIG, DataObject, ResourceObject
from jkit._constraints import (
    PositiveFloat,
    PositiveInt,
    UserName,
    UserSlug,
    UserUploadedUrl,
)
from jkit._network_request import get_json
from jkit._normalization import normalize_assets_amount
from jkit.config import CONFIG
from jkit.exceptions import APIUnsupportedError

if TYPE_CHECKING:
    from jkit.user import User


class UserEarningRankRecord(DataObject, **DATA_OBJECT_CONFIG):
    ranking: PositiveInt
    name: UserName
    slug: UserSlug
    avatar_url: UserUploadedUrl
    total_fp_amount: PositiveFloat
    fp_by_creating_anount: PositiveFloat
    fp_by_voting_amount: PositiveFloat

    def to_user_obj(self) -> "User":
        from jkit.user import User

        return User.from_slug(self.slug)._as_checked()


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
            raise APIUnsupportedError("不支持获取 2020.06.20 前的排行榜数据")
        if target_date >= datetime.now().date():
            raise ValueError("不支持获取未来的排行榜数据")

        self._target_date = target_date
        self._type = type

    async def get_data(self) -> UserEarningRankData:
        data = await get_json(
            endpoint=CONFIG.endpoints.jianshu,
            path="/asimov/fp_rankings/voter_users",
            params={
                "type": {"all": None, "creating": "note", "voting": "like"}[self._type],
                "date": self._target_date.strftime(r"%Y%m%d"),
            },
        )
        print(data["users"][2])

        return UserEarningRankData(
            total_fp_amount_sum=normalize_assets_amount(data["fp"]),
            fp_by_creating_amount_sum=normalize_assets_amount(data["author_fp"]),
            fp_by_voting_amount_sum=normalize_assets_amount(data["voter_fp"]),
            records=tuple(
                UserEarningRankRecord(
                    ranking=ranking,
                    name=item["nickname"],
                    slug=item["slug"],
                    avatar_url=item["avatar"],
                    total_fp_amount=normalize_assets_amount(item["fp"]),
                    fp_by_creating_anount=normalize_assets_amount(item["author_fp"]),
                    fp_by_voting_amount=normalize_assets_amount(item["voter_fp"]),
                )
                for ranking, item in enumerate(data["users"], start=1)
            ),
        )._validate()

    async def __aiter__(self) -> AsyncGenerator[UserEarningRankRecord, None]:
        for item in (await self.get_data()).records:
            yield item
