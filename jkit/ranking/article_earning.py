from datetime import date, datetime
from typing import TYPE_CHECKING, Optional, Tuple

from jkit._base import DATA_OBJECT_CONFIG, DataObject, RankingResourceObject
from jkit._constraints import (
    ArticleSlugStr,
    NonEmptyStr,
    PositiveFloat,
    PositiveInt,
    UserNameStr,
    UserUploadedUrlStr,
)
from jkit._http_client import get_json
from jkit._normalization import normalize_assets_amount
from jkit.config import ENDPOINT_CONFIG
from jkit.exceptions import APIUnsupportedError

if TYPE_CHECKING:
    from jkit.article import Article


class ArticleEarningRankRecordUserInfo(DataObject, **DATA_OBJECT_CONFIG):
    name: Optional[UserNameStr]
    avatar_url: Optional[UserUploadedUrlStr]


class ArticleEarningRankRecord(DataObject, **DATA_OBJECT_CONFIG):
    ranking: PositiveInt
    title: Optional[NonEmptyStr]
    slug: Optional[ArticleSlugStr]
    total_fp_amount: PositiveFloat
    fp_to_author_anount: PositiveFloat
    fp_to_voter_amount: PositiveFloat
    user_info: ArticleEarningRankRecordUserInfo

    @property
    def is_missing(self) -> bool:
        return not bool(self.slug)

    def get_article_obj(self) -> "Article":
        if not self.slug:
            raise APIUnsupportedError("文章走丢了，无法获取文章对象")

        from jkit.article import Article

        return Article.from_slug(self.slug)


class ArticleEarningRankData(DataObject, **DATA_OBJECT_CONFIG):
    total_fp_amount_sum: PositiveFloat
    fp_to_author_amount_sum: PositiveFloat
    fp_to_voter_amount_sum: PositiveFloat
    records: Tuple[ArticleEarningRankRecord, ...]


class ArticleEarningRank(RankingResourceObject):
    def __init__(self, target_date: date, /) -> None:
        if target_date < date(2020, 6, 20):
            raise APIUnsupportedError("仅支持获取 2020.06.20 后的排行榜数据")
        if target_date >= datetime.now().date():
            raise ValueError("不支持获取尚未生成的排行榜数据")

        self._target_date = target_date

    async def get_data(self) -> ArticleEarningRankData:
        data = await get_json(
            endpoint=ENDPOINT_CONFIG.jianshu,
            path="/asimov/fp_rankings/voter_notes",
            params={"date": self._target_date.strftime(r"%Y%m%d")},
        )

        return ArticleEarningRankData(
            total_fp_amount_sum=normalize_assets_amount(data["fp"]),
            fp_to_author_amount_sum=normalize_assets_amount(data["author_fp"]),
            fp_to_voter_amount_sum=normalize_assets_amount(data["voter_fp"]),
            records=tuple(
                ArticleEarningRankRecord(
                    ranking=ranking,
                    title=item["title"],
                    slug=item["slug"],
                    total_fp_amount=normalize_assets_amount(item["fp"]),
                    fp_to_author_anount=normalize_assets_amount(item["author_fp"]),
                    fp_to_voter_amount=normalize_assets_amount(item["voter_fp"]),
                    user_info=ArticleEarningRankRecordUserInfo(
                        name=item["author_nickname"],
                        avatar_url=item["author_avatar"],
                    ),
                )
                for ranking, item in enumerate(data["notes"], start=1)
            ),
        )._validate()
