from decimal import Context, Decimal
from typing import AsyncGenerator, Literal, Optional

from jkit._base import DATA_OBJECT_CONFIG, DataObject, ResourceObject
from jkit._constraints import (
    NonEmptyStr,
    NormalizedDatetime,
    PositiveInt,
)
from jkit._network_request import get_json
from jkit._normalization import normalize_assets_amount, normalize_datetime
from jkit.config import ENDPOINT_CONFIG
from jkit.credential import JianshuCredential


class AssetsTransactionRecord(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt  # noqa: A003
    time: NormalizedDatetime
    type_id: PositiveInt
    type_text: NonEmptyStr
    amount: float
    amount_precise: Decimal


class AssetsTransactionHistory(ResourceObject):
    def __init__(
        self, *, credential: JianshuCredential, assets_type: Literal["FP", "FTN"]
    ) -> None:
        self._credential = credential
        self._assets_type = assets_type

    async def iter_records(
        self, max_id: Optional[int] = None
    ) -> AsyncGenerator[AssetsTransactionRecord, None]:
        now_max_id = max_id

        while True:
            data = await get_json(
                endpoint=ENDPOINT_CONFIG.jianshu,
                path={
                    "FP": "/asimov/fp_wallets/transactions",
                    "FTN": "/asimov/fp_wallets/jsb_transactions",
                }[self._assets_type],
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
                yield AssetsTransactionRecord(
                    id=item["id"],
                    time=normalize_datetime(item["time"]),
                    type_id=item["tn_type"],
                    type_text=item["display_name"],
                    amount=normalize_assets_amount(item["amount"])
                    * (-1 if is_out else 1),
                    amount_precise=Context(prec=18).create_decimal_from_float(
                        (item["amount_18"] * (-1 if is_out else 1)) / 10**18
                    ),
                )._validate()
