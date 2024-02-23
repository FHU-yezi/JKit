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


class UserInfoField(DataObject, **DATA_OBJECT_CONFIG):
    id: Optional[PositiveInt]
    slug: Optional[UserSlug]
    name: Optional[UserName]
    avatar_url: Optional[UserUploadedUrl]

    def to_user_obj(self) -> "User":
        from jkit.user import User

        if not self.slug:
            raise ResourceUnavailableError("用户已注销或被封禁")

        return User.from_slug(self.slug)._as_checked()


class AssetsRankingRecord(DataObject, **DATA_OBJECT_CONFIG):
    ranking: PositiveInt
    assets_amount: NonNegativeFloat
    user_info: UserInfoField


class AssetsRanking(ResourceObject):
    def __init__(self, *, start_id: int = 1) -> None:
        self._start_id = start_id

    async def __aiter__(self) -> AsyncGenerator[AssetsRankingRecord, None]:
        now_id = self._start_id
        while True:
            data = await get_json(
                endpoint=CONFIG.endpoints.jianshu,
                path="/asimov/fp_rankings",
                params={"since_id": now_id - 1, "max_id": MAX_ID},
            )
            if not data["rankings"]:
                return

            for item in data["rankings"]:
                yield AssetsRankingRecord(
                    ranking=item["ranking"],
                    assets_amount=normalize_assets_amount(item["amount"]),
                    user_info=UserInfoField(
                        id=item["user"]["id"],
                        slug=item["user"]["slug"],
                        name=item["user"]["nickname"],
                        avatar_url=item["user"]["avatar"],
                    ),
                )._validate()

            now_id += len(data["rankings"])
