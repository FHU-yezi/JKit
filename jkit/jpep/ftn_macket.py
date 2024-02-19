from enum import Enum
from typing import AsyncGenerator, Literal, Optional, Tuple

from jkit._base import DATA_OBJECT_CONFIG, DataObject, ResourceObject
from jkit._constraints import (
    NonEmptyStr,
    NonNegativeInt,
    NormalizedDatetime,
    PositiveFloat,
    PositiveInt,
)
from jkit._network_request import send_post
from jkit._normalization import normalize_datetime
from jkit.config import CONFIG


class PaymentChannels(Enum):
    WECHAT_PAY = "微信支付"
    ALIPAY = "支付宝"
    ANT_CREDIT_PAY = "蚂蚁花呗"


class FTNMacketOrderPublisherInfo(DataObject, **DATA_OBJECT_CONFIG):
    is_anonymous: bool
    id: Optional[PositiveInt]
    name: Optional[NonEmptyStr]
    hashed_name: Optional[NonEmptyStr]
    avatar_url: Optional[NonEmptyStr]
    credit: Optional[NonNegativeInt]


class FTNMacketOrder(DataObject, **DATA_OBJECT_CONFIG):
    id: PositiveInt
    price: PositiveFloat

    total_amount: PositiveInt
    traded_amount: NonNegativeInt
    tradable_amount: NonNegativeInt
    minimum_trade_amount: PositiveInt

    traded_count: NonNegativeInt
    publish_time: NormalizedDatetime
    supported_payment_channels: Tuple[PaymentChannels, ...]

    publisher_info: FTNMacketOrderPublisherInfo


class FTNMacket(ResourceObject):
    async def iter_orders(
        self,
        *,
        type: Literal["buy", "sell"],  # noqa: A002
        start_page: int = 1,
    ) -> AsyncGenerator[FTNMacketOrder, None]:
        now_page = start_page
        while True:
            data = await send_post(
                endpoint=CONFIG.endpoints.jpep,
                path="/getList/furnish.bei/",
                params={"page": now_page},
                json={
                    "filter": [
                        {"trade": 1 if type == "buy" else 0},
                        {"status": 1},
                        {"finish": 0},
                        {"tradable": {">": "0"}},
                    ],
                    "sort": "price,pub_date" if type == "buy" else "-price,pub_date",
                    "bind": [
                        {
                            "member.user": {
                                "filter": [{"id": "{{uid}}"}],
                                "addField": [{"username_md5": "username_md5"}],
                                "fields": "id,username,avatarUrl,credit,pay_types",
                            }
                        }
                    ],
                    "addField": [
                        {"tradeCount": "tradeCount"},
                        {"tradeNum": "tradeNum"},
                    ],
                },
            )

            if not data["data"]:
                break

            for item in data["data"]:
                yield FTNMacketOrder(
                    id=item["id"],
                    price=item["price"],
                    total_amount=item["totalNum"],
                    traded_amount=item["tradeNum"],
                    tradable_amount=item["tradable"],
                    minimum_trade_amount=item["minNum"],
                    traded_count=item["tradeCount"],
                    publish_time=normalize_datetime(item["pub_date"]),
                    supported_payment_channels=tuple(
                        {
                            1: PaymentChannels.WECHAT_PAY,
                            2: PaymentChannels.ALIPAY,
                            3: PaymentChannels.ANT_CREDIT_PAY,
                        }[int(x)]
                        for x in item["member.user"][0]["pay_types"].split("|")
                    )
                    if item["member.user"][0]["pay_types"]
                    else (),
                    publisher_info=FTNMacketOrderPublisherInfo(
                        is_anonymous=bool(item["anony"]),
                        id=item["member.user"][0]["id"],
                        name=item["member.user"][0]["username"],
                        hashed_name=item["member.user"][0]["username_md5"],
                        avatar_url=item["member.user"][0]["avatarUrl"]
                        if item["member.user"][0]["avatarUrl"]
                        else None,
                        credit=item["member.user"][0]["credit"],
                    ),
                )

            now_page += 1
