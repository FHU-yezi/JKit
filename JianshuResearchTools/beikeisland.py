import json

import requests

from basic import BeikeIsland_request_header
from convert import UserUrlToUserSlug


def GetBeikeIslandTotalTradeAmount() -> int:
    # TODO: 注释优化
    """该函数返回贝壳小岛的总交易额。

    Returns:
        int: 总交易额
    """
    data = {}  # 不传送数据也能正常获取，节省时间和带宽
    source = requests.post("https://www.beikeisland.com/api/Trade/getTradeRankList", 
                            headers=BeikeIsland_request_header, json=data)
    json_obj = json.loads(source.content)
    result = json_obj["data"]["totalcount"]
    return result

def GetBeikeIslandTotalTradeCount() -> int:
    # TODO: 注释优化
    """该函数返回贝壳小岛的总交易次数。

    Returns:
        int: 总交易次数
    """
    data = {}  # 不传送数据也能正常获取，节省时间和带宽
    source = requests.post("https://www.beikeisland.com/api/Trade/getTradeRankList", 
                            headers=BeikeIsland_request_header, json=data)
    json_obj = json.loads(source.content)
    result = json_obj["data"]["totaltime"]
    return result

def GetBeikeIslandTotalTradeRankInfo(page: int =1) -> list:
    """该函数接收一个页码参数，并返回贝壳小岛总交易排行榜中对应页码的用户信息

    Args:
        page (int, optional): 排行榜页码. Defaults to 1.

    Returns:
        list: 总交易排行榜中对应页码的用户信息
    """
    data = {
        "ranktype": 3, 
        "pageIndex": page
    }
    source = requests.post("https://www.beikeisland.com/api/Trade/getTradeRankList", 
                            headers=BeikeIsland_request_header, json=data)
    json_obj = json.loads(source.content)
    result = []
    for item in json_obj["data"]["ranklist"]:
        item_info = {
            "bkuid": item["userid"], 
            "jianshuname": item["jianshuname"], 
            "avatar": item["avatarurl"], 
            "userurl": item["jianshupath"], 
            "uslug": UserUrlToUserSlug(item["jianshupath"]), 
            "total_trade_amount": item["totalamount"], 
            "total_trade_times": item["totaltime"]
        }
        result.append(item_info)
    return result

def GetBeikeIslandBuyTradeRankInfo(page: int =1) -> list:
    """该函数接收一个页码参数，并返回贝壳小岛买贝排行榜中对应页码的用户信息

    Args:
        page (int, optional): 排行榜页码. Defaults to 1.

    Returns:
        list: 买贝排行榜中对应页码的用户信息
    """
    data = {
        "ranktype": 1, 
        "pageIndex": page
    }
    source = requests.post("https://www.beikeisland.com/api/Trade/getTradeRankList", 
                            headers=BeikeIsland_request_header, json=data)
    json_obj = json.loads(source.content)
    result = []
    for item in json_obj["data"]["ranklist"]:
        item_info = {
            "bkuid": item["userid"], 
            "jianshuname": item["jianshuname"], 
            "avatar": item["avatarurl"], 
            "userurl": item["jianshupath"], 
            "uslug": UserUrlToUserSlug(item["jianshupath"]), 
            "total_trade_amount": item["totalamount"], 
            "total_trade_times": item["totaltime"]
        }
        result.append(item_info)
    return result

def GetBeikeIslandSellTradeRankInfo(page: int =1) -> list:
    """该函数接收一个页码参数，并返回贝壳小岛卖贝排行榜中对应页码的用户信息

    Args:
        page (int, optional): 排行榜页码. Defaults to 1.

    Returns:
        list: 卖贝排行榜中对应页码的用户信息
    """
    data = {
        "ranktype": 2, 
        "pageIndex": page
    }
    source = requests.post("https://www.beikeisland.com/api/Trade/getTradeRankList", 
                            headers=BeikeIsland_request_header, json=data)
    json_obj = json.loads(source.content)
    result = []
    for item in json_obj["data"]["ranklist"]:
        item_info = {
            "bkuid": item["userid"], 
            "jianshuname": item["jianshuname"], 
            "avatar": item["avatarurl"], 
            "userurl": item["jianshupath"], 
            "uslug": UserUrlToUserSlug(item["jianshupath"]), 
            "total_trade_amount": item["totalamount"], 
            "total_trade_times": item["totaltime"]
        }
        result.append(item_info)
    return result