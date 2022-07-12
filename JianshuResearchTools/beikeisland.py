from datetime import datetime
from typing import Dict, List

from .basic_apis import (GetBeikeIslandTradeListJsonDataApi,
                         GetBeikeIslandTradeRankListJsonDataApi)
from .convert import UserUrlToUserSlug
from .exceptions import ResourceError

__all__ = [
    "GetBeikeIslandTotalTradeAmount", "GetBeikeIslandTotalTradeCount",
    "GetBeikeIslandTotalTradeRankData", "GetBeikeIslandBuyTradeRankData",
    "GetBeikeIslandSellTradeRankData", "GetBeikeIslandTradeOrderInfo",
    "GetBeikeIslandTradePrice"
]


def GetBeikeIslandTotalTradeAmount() -> int:
    """获取贝壳小岛总交易量

    Returns:
        int: 总交易量
    """
    json_obj = GetBeikeIslandTradeRankListJsonDataApi(ranktype=None, pageIndex=None)
    result = json_obj["data"]["totalcount"]
    return result


def GetBeikeIslandTotalTradeCount() -> int:
    """获取贝壳小岛总交易笔数

    Returns:
        int: 总交易笔数
    """
    json_obj = GetBeikeIslandTradeRankListJsonDataApi(ranktype=None, pageIndex=None)
    result = json_obj["data"]["totaltime"]
    return result


def GetBeikeIslandTotalTradeRankData(page: int = 1) -> List[Dict]:
    """获取贝壳小岛总交易排行榜中的用户信息

    Args:
        page (int, optional): 页码. Defaults to 1.

    Returns:
        List: 总交易排行榜的用户信息
    """
    json_obj = GetBeikeIslandTradeRankListJsonDataApi(ranktype=3, pageIndex=page)
    result = []
    for item in json_obj["data"]["ranklist"]:
        item_data = {
            "bkuid": item["userid"],
            "jianshuname": item["jianshuname"],
            "avatar_url": item["avatarurl"],
            "userurl": item["jianshupath"],
            "uslug": UserUrlToUserSlug(item["jianshupath"]),
            "total_trade_amount": item["totalamount"],
            "total_trade_times": item["totaltime"]
        }
        result.append(item_data)
    return result


def GetBeikeIslandBuyTradeRankData(page: int = 1) -> List[Dict]:
    """获取贝壳小岛买贝排行榜中的用户信息

    Args:
        page (int, optional): 页码. Defaults to 1.

    Returns:
        List: 买贝榜的用户信息
    """
    json_obj = GetBeikeIslandTradeRankListJsonDataApi(ranktype=1, pageIndex=page)
    result = []
    for item in json_obj["data"]["ranklist"]:
        item_data = {
            "bkuid": item["userid"],
            "jianshuname": item["jianshuname"],
            "avatar_url": item["avatarurl"],
            "userurl": item["jianshupath"],
            "uslug": UserUrlToUserSlug(item["jianshupath"]),
            "total_trade_amount": item["totalamount"],
            "total_trade_times": item["totaltime"]
        }
        result.append(item_data)
    return result


def GetBeikeIslandSellTradeRankData(page: int = 1) -> List[Dict]:
    """获取贝壳小岛卖贝排行榜中的用户信息

    Args:
        page (int, optional): 页码. Defaults to 1.

    Returns:
        List: 卖贝榜的用户信息
    """
    json_obj = GetBeikeIslandTradeRankListJsonDataApi(ranktype=2, pageIndex=page)
    result = []
    for item in json_obj["data"]["ranklist"]:
        item_data = {
            "bkuid": item["userid"],
            "jianshuname": item["jianshuname"],
            "avatar_url": item["avatarurl"],
            "userurl": item["jianshupath"],
            "uslug": UserUrlToUserSlug(item["jianshupath"]),
            "total_trade_amount": item["totalamount"],
            "total_trade_times": item["totaltime"]
        }
        result.append(item_data)
    return result


def GetBeikeIslandTradeOrderInfo(trade_type: str, page: int = 1) -> List[Dict]:
    """获取贝壳小岛的挂单信息

    Args:
        trade_type (str): 为 "buy" 时获取买单信息，为 "sell" 时获取卖单信息
        page (int, optional): 页码. Defaults to 1.

    Returns:
        List: 挂单数据
    """
    # 通过 trade_type 构建 retype
    retype = {
        "buy": 2,
        "sell": 1
    }[trade_type]
    json_obj = GetBeikeIslandTradeListJsonDataApi(pageIndex=page,
                                                  retype=retype)
    result = []
    for item in json_obj["data"]["tradelist"]:
        item_data = {
            "trade_id": item["id"],
            "trade_slug": item["tradeno"],
            "publish_time": datetime.fromisoformat(item["releasetime"]),
            "status": {
                "code": item["statuscode"],
                "text": item["statustext"]
            },
            "trade": {
                "total": item["recount"],
                "traded": item["recount"] - item["cantradenum"],
                "remaining": item["cantradenum"],
                "minimum_trade_limit": item["minlimit"],
                "traded_percentage": round(
                    float(item["compeletper"]) / 100, 3
                ),
                "price": item["reprice"],
            }
        }

        if item["anonymity"]:
            item_data["user"] = {
                "is_anonymity": True
            }
        else:
            item_data["user"] = {
                "is_anonymity": False,
                "name": item["reusername"],
                "avatar_url": item["avatarurl"],
                "level": {
                    "code": item["levelnum"],
                    "text": item["userlevel"]
                }
            }

        result.append(item_data)
    return result


def GetBeikeIslandTradePrice(trade_type: str, rank: int = 1) -> float:
    """获取特定位置交易单的价格

    Args:
        trade_type (str): trade_type (str): 为 "buy" 时获取买单信息，为 "sell" 时获取卖单信息
        rank (int, optional): 自最低 / 最高价开始，需要获取的价格所在的位置. Defaults to 1.

    Returns:
        float: 交易单的价格
    """
    pageIndex = int(rank / 10)  # 确定需要请求的页码
    # 通过 trade_type 构建 retype
    retype = {
        "buy": 2,
        "sell": 1
    }[trade_type]
    json_obj = GetBeikeIslandTradeListJsonDataApi(pageIndex=pageIndex, retype=retype)
    rank_in_this_page = rank % 10 - 1  # 本页信息中目标交易单的位置，考虑索引下标起始值为 0 问题
    try:
        result = json_obj["data"]["tradelist"][rank_in_this_page]["reprice"]
    except IndexError:
        raise ResourceError("该排名没有对应的交易单")
    return result
