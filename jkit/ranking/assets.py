from typing import TYPE_CHECKING, AsyncGenerator, Optional

from jkit._base import DATA_OBJECT_CONFIG, DataObject, ResourceObject
from jkit._constraints import (
    NonNegativeFloat,
    PositiveInt,
    UserName,
    UserSlug,
    UserUploadedUrl,
)
from jkit._network_request import get_json
from jkit._normalization import normalize_assets_amount
from jkit.config import CONFIG
from jkit.constants import MAX_ID
from jkit.exceptions import ResourceUnavailableError

if TYPE_CHECKING:
    from jkit.user import User


class AssetsRankRecordUserInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: Optional[PositiveInt]
    slug: Optional[UserSlug]
    name: Optional[UserName]
    avatar_url: Optional[UserUploadedUrl]

    def to_user_obj(self) -> "User":
        from jkit.user import User

        if not self.slug:
            raise ResourceUnavailableError("用户信息不可用，无法生成用户对象")

        return User.from_slug(self.slug)._as_checked()


class AssetsRankRecord(DataObject, **DATA_OBJECT_CONFIG):
    ranking: PositiveInt
    assets_amount: NonNegativeFloat
    user_info: AssetsRankRecordUserInfo


class AssetsRank(ResourceObject):
    async def iter_data(
        self, *, start_id: int = 1
    ) -> AsyncGenerator[AssetsRankRecord, None]:
        now_id = start_id
        while True:
            data = await get_json(
                endpoint=CONFIG.endpoints.jianshu,
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
                        name=item["user"]["nickname"],
                        avatar_url=item["user"]["avatar"],
                    ),
                )._validate()

            now_id += len(data["rankings"])
