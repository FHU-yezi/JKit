from jkit._base import DATA_OBJECT_CONFIG, DataObject, ResourceObject
from jkit._constraints import NonNegativeFloat
from jkit._network_request import send_post
from jkit.config import CONFIG


class PlatformSettingsInfo(DataObject, **DATA_OBJECT_CONFIG):
    opening: bool

    ftn_trade_fee: NonNegativeFloat
    goods_trade_fee: NonNegativeFloat

    ftn_buy_trade_minimum_price: NonNegativeFloat
    ftn_sell_trade_minimum_price: NonNegativeFloat


class PlatformSettings(ResourceObject):
    async def get_data(self) -> PlatformSettingsInfo:
        data = await send_post(
            endpoint=CONFIG.endpoints.jpep,
            path="/getList/furnish.setting/1/",
            json={"fields": "isClose,fee,shop_fee,minimum_price,buy_minimum_price"},
        )

        return PlatformSettingsInfo(
            opening=not bool(data["data"]["isClose"]),
            ftn_trade_fee=data["data"]["fee"],
            goods_trade_fee=data["data"]["shop_fee"],
            ftn_buy_trade_minimum_price=data["data"]["buy_minimum_price"],
            ftn_sell_trade_minimum_price=data["data"]["minimum_price"],
        )._validate()
