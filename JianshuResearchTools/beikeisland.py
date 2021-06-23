import json
from datetime import datetime

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

def GetBeikeIslandTradeInfo(trade_type: str, page: int =1) -> list:
    """该函数接收一个交易类型字符串和一个页码参数，并返回贝壳小岛中该类型交易列表中对应页的交易信息

    Args:
        trade_type (str): 为 buy 时获取买单信息，为 sell 时获取卖单信息
        page (int, optional): 交易列表页码. Defaults to 1.

    Returns:
        list: 该类型交易列表中对应页的信息
    """
    data = {
        "pageIndex": page, 
        "retype": {
            "buy": 2, 
            "sell": 1
        }[trade_type]  # 通过 trade_type 构建 retype
    }
    source = requests.post("https://www.beikeisland.com/api/Trade/getTradeList", 
                            headers=BeikeIsland_request_header, json=data)
    json_obj = json.loads(source.content)
    result = []
    for item in json_obj["data"]["tradelist"]:
        item_info = { # TODO: 这里应该改成双层嵌套结构
            "tradeid": item["id"], 
            "tradeslug": item["tradeno"],   # ? 我也不确定这个 no 什么意思,回来去问问
            "bkname": item["reusername"],   # ? 还有个 nickname，不知道哪个对
            "jianshuname": item["jianshuname"], 
            "avatar": item["avatarurl"], 
            "total": item["recount"], 
            "traded": item["recount"] - item["cantradenum"], 
            "remaining": item["cantradenum"], 
            "price": item["reprice"], 
            "minimum_limit": item["minlimit"], 
            "percentage": item["compeletper"], 
            "statuscode": item["statuscode"], 
            "status": item["statustext"], 
            "userlevelcode": item["levelnum"], 
            "userlevel": item["userlevel"], 
            "user_trade_count": item["tradecount"], 
            "release_time": item["releasetime"]
        }
        result.append(item_info)
    return result

def GetBeikeIslandTradePrice(trade_type: str, rank: int =1) -> float:
    """该函数接收一个消息类型字符串和一个排名参数，并返回贝壳小岛交易列表中该类型对应位置交易单的交易价格

    Args:
        trade_type (str): 为 buy 时获取买单信息，为 sell 时获取卖单信息
        rank (int, optional): 该类型中目标价格的位置. Defaults to 1.

    Returns:
        float: 交易列表中该类型对应位置交易单的交易价格
    """
    data = {
        "pageIndex": int(rank / 10),  # 确定需要请求的页码
        "retype": {
            "buy": 2, 
            "sell": 1
        }[trade_type]  # 通过 trade_type 构建 retype
    }
    source = requests.post("https://www.beikeisland.com/api/Trade/getTradeList", 
                            headers=BeikeIsland_request_header, json=data)
    json_obj = json.loads(source.content)
    rank_in_this_page = rank % 10  # 本页信息中目标交易单的位置，考虑索引下标起始值为 0 问题
    result = json_obj["data"]["tradelist"][rank_in_this_page]["reprice"]
    return result