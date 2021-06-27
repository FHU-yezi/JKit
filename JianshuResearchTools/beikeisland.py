import json
from datetime import datetime

import requests

from convert import UserUrlToUserSlug
from headers import BeikeIsland_request_header


def GetBeikeIslandTotalTradeAmount() -> int:
    """获取贝壳小岛总交易量

    Returns:
        int: 总交易量
    """
    data = {}  # 不传送数据也能正常获取，节省时间和带宽
    source = requests.post("https://www.beikeisland.com/api/Trade/getTradeRankList", 
                            headers=BeikeIsland_request_header, json=data).content
    json_obj = json.loads(source)
    result = json_obj["data"]["totalcount"]
    return result

def GetBeikeIslandTotalTradeCount() -> int:
    """获取贝壳小岛总交易笔数

    Returns:
        int: 总交易笔数
    """
    data = {}  # 不传送数据也能正常获取，节省时间和带宽
    source = requests.post("https://www.beikeisland.com/api/Trade/getTradeRankList", 
                            headers=BeikeIsland_request_header, json=data).content
    json_obj = json.loads(source)
    result = json_obj["data"]["totaltime"]
    return result

def GetBeikeIslandTotalTradeRankData(page: int = 1) -> list:
    """获取贝壳小岛总交易排行榜中的用户数据

    Args:
        page (int, optional): 页码. Defaults to 1.

    Returns:
        list: 总交易排行榜的用户数据
    """
    data = {
        "ranktype": 3, 
        "pageIndex": page
    }
    source = requests.post("https://www.beikeisland.com/api/Trade/getTradeRankList", 
                            headers=BeikeIsland_request_header, json=data).content
    json_obj = json.loads(source)
    result = []
    for item in json_obj["data"]["ranklist"]:
        item_data = {
            "bkuid": item["userid"], 
            "jianshuname": item["jianshuname"], 
            "avatar": item["avatarurl"], 
            "userurl": item["jianshupath"], 
            "uslug": UserUrlToUserSlug(item["jianshupath"]), 
            "total_trade_amount": item["totalamount"], 
            "total_trade_times": item["totaltime"]
        }
        result.append(item_data)
    return result

def GetBeikeIslandBuyTradeRankData(page: int = 1) -> list:
    """获取贝壳小岛买贝排行榜中的用户数据

    Args:
        page (int, optional): 页码. Defaults to 1.

    Returns:
        list: 买贝榜的用户数据
    """
    data = {
        "ranktype": 1, 
        "pageIndex": page
    }
    source = requests.post("https://www.beikeisland.com/api/Trade/getTradeRankList", 
                            headers=BeikeIsland_request_header, json=data).content
    json_obj = json.loads(source)
    result = []
    for item in json_obj["data"]["ranklist"]:
        item_data = {
            "bkuid": item["userid"], 
            "jianshuname": item["jianshuname"], 
            "avatar": item["avatarurl"], 
            "userurl": item["jianshupath"], 
            "uslug": UserUrlToUserSlug(item["jianshupath"]), 
            "total_trade_amount": item["totalamount"], 
            "total_trade_times": item["totaltime"]
        }
        result.append(item_data)
    return result

def GetBeikeIslandSellTradeRankData(page: int = 1) -> list:
    """获取贝壳小岛卖贝排行榜中的用户数据

    Args:
        page (int, optional): 页码. Defaults to 1.

    Returns:
        list: 卖贝榜的用户数据
    """
    data = {
        "ranktype": 2, 
        "pageIndex": page
    }
    source = requests.post("https://www.beikeisland.com/api/Trade/getTradeRankList", 
                            headers=BeikeIsland_request_header, json=data).content
    json_obj = json.loads(source)
    result = []
    for item in json_obj["data"]["ranklist"]:
        item_data = {
            "bkuid": item["userid"], 
            "jianshuname": item["jianshuname"], 
            "avatar": item["avatarurl"], 
            "userurl": item["jianshupath"], 
            "uslug": UserUrlToUserSlug(item["jianshupath"]), 
            "total_trade_amount": item["totalamount"], 
            "total_trade_times": item["totaltime"]
        }
        result.append(item_data)
    return result

def GetBeikeIslandTradeOrderInfo(trade_type: str, page: int = 1) -> list:
    """获取贝壳小岛的挂单信息

    Args:
        trade_type (str): buy 为买单，sell 为卖单
        page (int, optional): 页码. Defaults to 1.

    Returns:
        list: 挂单数据
    """
    data = {
        "pageIndex": page, 
        "retype": {
            "buy": 2, 
            "sell": 1
        }[trade_type]  # 通过 trade_type 构建 retype
    }
    source = requests.post("https://www.beikeisland.com/api/Trade/getTradeList", 
                            headers=BeikeIsland_request_header, json=data).content
    json_obj = json.loads(source)
    result = []
    for item in json_obj["data"]["tradelist"]:
        item_data = { # TODO: 这里应该改成双层嵌套结构
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
        result.append(item_data)
    return result

def GetBeikeIslandTradePrice(trade_type: str, rank: int = 1) -> float:
    """获取特定位置交易单的价格

    Args:
        trade_type (str): buy 为买单，sell 为卖单
        rank (int, optional): 自最低 / 最高价开始，需要获取的价格所在的位置. Defaults to 1.

    Returns:
        float: 交易单的价格
    """
    data = {
        "pageIndex": int(rank / 10),  # 确定需要请求的页码
        "retype": {
            "buy": 2, 
            "sell": 1
        }[trade_type]  # 通过 trade_type 构建 retype
    }
    source = requests.post("https://www.beikeisland.com/api/Trade/getTradeList", 
                            headers=BeikeIsland_request_header, json=data).content
    json_obj = json.loads(source)
    rank_in_this_page = rank % 10  # 本页信息中目标交易单的位置，考虑索引下标起始值为 0 问题
    result = json_obj["data"]["tradelist"][rank_in_this_page]["reprice"]
    return result
