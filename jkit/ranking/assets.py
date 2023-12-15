from typing import TYPE_CHECKING, AsyncGenerator, Tuple

from jkit._base import DATA_OBJECT_CONFIG, DataObject, ResourceObject
from jkit._constraints import (
    NonNegativeFloat,
    PositiveInt,
    UserSlugStr,
    UserUploadedUrlStr,
)
from jkit._http_client import get_json
from jkit.config import ENDPOINT_CONFIG
from jkit.constants import MAX_ID

if TYPE_CHECKING:
    from jkit.user import User


class AssetsRankItemUserInfo(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt  # noqa: A003
    slug: UserSlugStr
    avatar_url: UserUploadedUrlStr

    def get_user_obj(self) -> "User":
        from jkit.user import User

        return User.from_slug(self.slug)


class AssetsRankItem(DataObject, **DATA_OBJECT_CONFIG):
    ranking: PositiveInt
    assert_amount: NonNegativeFloat
    user_info: AssetsRankItemUserInfo


# TODO: 支持获取完整数据
class AssetsRank(ResourceObject):
    def __init__(self, *, full: bool = False) -> None:
        self._full = full

    async def get_data(self, *, start_id: int = 1) -> Tuple[AssetsRankItem, ...]:
        data = await get_json(
            endpoint=ENDPOINT_CONFIG.jianshu,
            path="/asimov/fp_rankings",
            params={"since_id": start_id - 1, "max_id": MAX_ID},
        )

        return tuple(
            AssetsRankItem(
                ranking=item["ranking"],
                assert_amount=item["amount"],
                user_info=AssetsRankItemUserInfo(
                    id=item["user"]["id"],
                    slug=item["user"]["slug"],
                    avatar_url=item["user"]["avatar"],
                ),
            ).validate()
            for item in data["rankings"]
        )

    async def iter_data(
        self, start_id: int = 1
    ) -> AsyncGenerator[AssetsRankItem, None]:
        now_id = start_id
        while True:
            data = await self.get_data(start_id=now_id)
            for item in data:
                yield item

            now_id += len(data)
