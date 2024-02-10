from typing import TYPE_CHECKING, AsyncGenerator

from jkit._base import DATA_OBJECT_CONFIG, DataObject, RankingResourceObject
from jkit._constraints import (
    NonNegativeFloat,
    PositiveInt,
    UserSlugStr,
    UserUploadedUrlStr,
)
from jkit._network_request import get_json
from jkit._normalization import normalize_assets_amount
from jkit.config import ENDPOINT_CONFIG
from jkit.constants import MAX_ID

if TYPE_CHECKING:
    from jkit.user import User


class AssetsRankRecordUserInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt
    slug: UserSlugStr
    avatar_url: UserUploadedUrlStr

    def to_user_obj(self) -> "User":
        from jkit.user import User

        return User.from_slug(self.slug)._from_trusted_source()


class AssetsRankRecord(DataObject, **DATA_OBJECT_CONFIG):
    ranking: PositiveInt
    assets_amount: NonNegativeFloat
    user_info: AssetsRankRecordUserInfo


class AssetsRank(RankingResourceObject):
    async def iter_data(
        self, *, start_id: int = 1
    ) -> AsyncGenerator[AssetsRankRecord, None]:
        now_id = start_id
        while True:
            data = await get_json(
                endpoint=ENDPOINT_CONFIG.jianshu,
                path="/asimov/fp_rankings",
                params={"since_id": now_id - 1, "max_id": MAX_ID},
            )
            if not data["rankings"]:
                return

            for item in data["rankings"]:
                yield AssetsRankRecord(
                    ranking=item["ranking"],
                    assets_amount=normalize_assets_amount(item["amount"]),
                    user_info=AssetsRankRecordUserInfo(
                        id=item["user"]["id"],
                        slug=item["user"]["slug"],
                        avatar_url=item["user"]["avatar"],
                    ),
                )._validate()

            now_id += len(data["rankings"])
