from decimal import Decimal
from typing import AsyncGenerator, Optional

from jkit._base import DATA_OBJECT_CONFIG, DataObject, ResourceObject
from jkit._constraints import (
    NonEmptyStr,
    NormalizedDatetime,
    PositiveInt,
)
from jkit._network_request import get_json
from jkit._normalization import (
    normalize_assets_amount,
    normalize_assets_amount_precise,
    normalize_datetime,
)
from jkit.config import ENDPOINT_CONFIG
from jkit.credential import JianshuCredential


class AssetsTransactionHistoryRecord(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt  # noqa: A003
    time: NormalizedDatetime
    type_id: PositiveInt
    type_text: NonEmptyStr
    amount: float
    amount_precise: Decimal


class AssetsTransactionHistory(ResourceObject):
    def __init__(self, *, credential: JianshuCredential) -> None:
        self._credential = credential

    async def iter_fp_records(
        self, *, max_id: Optional[int] = None
    ) -> AsyncGenerator[AssetsTransactionHistoryRecord, None]:
        now_max_id = max_id

        while True:
            data = await get_json(
                endpoint=ENDPOINT_CONFIG.jianshu,
                path="/asimov/fp_wallets/transactions",
                params={"since_id": 0, "max_id": now_max_id}
                if now_max_id
                else {"since_id": 0},
                cookies=self._credential.cookies,
            )
            if not data["transactions"]:
                return

            now_max_id = data["transactions"][-1]["id"]

            for item in data["transactions"]:
                is_out = item["io_type"] == 2
                yield AssetsTransactionHistoryRecord(
                    id=item["id"],
                    time=normalize_datetime(item["time"]),
                    type_id=item["tn_type"],
                    type_text=item["display_name"],
                    amount=normalize_assets_amount(item["amount"])
                    * (-1 if is_out else 1),
                    amount_precise=normalize_assets_amount_precise(
                        item["amount_18"] * (-1 if is_out else 1)
                    ),
                )._validate()

    async def iter_ftn_records(
        self, *, max_id: Optional[int] = None
    ) -> AsyncGenerator[AssetsTransactionHistoryRecord, None]:
        now_max_id = max_id

        while True:
            data = await get_json(
                endpoint=ENDPOINT_CONFIG.jianshu,
                path="/asimov/fp_wallets/jsb_transactions",
                params={"since_id": 0, "max_id": now_max_id}
                if now_max_id
                else {"since_id": 0},
                cookies=self._credential.cookies,
            )
            if not data["transactions"]:
                return

            now_max_id = data["transactions"][-1]["id"]

            for item in data["transactions"]:
                is_out = item["io_type"] == 2
                yield AssetsTransactionHistoryRecord(
                    id=item["id"],
                    time=normalize_datetime(item["time"]),
                    type_id=item["tn_type"],
                    type_text=item["display_name"],
                    amount=normalize_assets_amount(item["amount"])
                    * (-1 if is_out else 1),
                    amount_precise=normalize_assets_amount_precise(
                        item["amount_18"] * (-1 if is_out else 1)
                    ),
                )._validate()


class FPRewardsHistoryRecord(DataObject, **DATA_OBJECT_CONFIG):
    time: NormalizedDatetime
    own_amount: Decimal
    referral_amount: Decimal
    grand_referral_amount: Decimal
    total_amount: Decimal


class FPRewardsHistory(ResourceObject):
    def __init__(self, *, credential: JianshuCredential) -> None:
        self._credential = credential

    async def iter_records(
        self, page_size: int = 10
    ) -> AsyncGenerator[FPRewardsHistoryRecord, None]:
        now_page = 1

        while True:
            data = await get_json(
                endpoint=ENDPOINT_CONFIG.jianshu,
                path="/asimov/fp_wallets/jsd_rewards",
                params={"page": now_page, "count": page_size},
                cookies=self._credential.cookies,
            )
            if not data["transactions"]:
                return

            for item in data["transactions"]:
                yield FPRewardsHistoryRecord(
                    time=normalize_datetime(item["time"]),
                    own_amount=normalize_assets_amount_precise(item["own_reards18"]),
                    referral_amount=normalize_assets_amount_precise(
                        item["referral_rewards18"]
                    ),
                    grand_referral_amount=normalize_assets_amount_precise(
                        item["grand_referral_rewards18"]
                    ),  # TODO: 命名调整
                    total_amount=normalize_assets_amount_precise(
                        item["total_amount18"]
                    ),
                )._validate()

            now_page += 1
