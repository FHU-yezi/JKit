import requests
import json
from assert_funcs import AssertJianshuUrl
from basic import jianshu_request_header
from convert import UserSlugToUserUrl
from user import GetUserAssetsCount
from exceptions import APIException

def GetAssetsRankData(start_id: int =1, get_full: bool =False) -> list:
    """该函数接收一个起始位置参数和一个获取全部数据的布尔值，并返回自该位置后 20 名用户的资产数据

    Args:
        start_id (int, optional): 起始位置. Defaults to 1.
        get_full (bool, optional): 为 True 时获取简书贝和总资产数据，为 False 时不获取. Defaults to False.

    Returns:
        list: 用户资产数据
    """
    start_id -= 1  # 索引下标为 0
    params = {
        "max_id": 1000000000,   # 与官方接口数值相同
        "since_id": start_id
    }
    source = requests.get("https://www.jianshu.com/asimov/fp_rankings", params=params, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    result = []
    for item in json_obj["rankings"]:
        item_info = {
            "ranking": item["ranking"], 
            "uid": item["user"]["id"], 
            "uslug": item["user"]["slug"], 
            "name": item["user"]["avatar"], 
            "FP": item["amount"] / 1000
        }
        if get_full == True:
            user_url = UserSlugToUserUrl(item_info["uslug"])
            try:
                item_info["Assets"] = GetUserAssetsCount(user_url)
                item_info["FTN"] =  round(item_info["Assets"] - item_info["FP"], 3) # 处理浮点数精度问题
            except APIException:
                pass
        result.append(item_info)
    return result

def GetDailyArticleRankData() -> list:
    """该函数返回日更排行榜的用户信息

    Returns:
        list: 日更排行榜用户信息
    """
    source = requests.get("https://www.jianshu.com/asimov/daily_activity_participants/rank", headers=jianshu_request_header).content
    json_obj = json.loads(source)
    result = []
    for item in json_obj["daps"]:
        item_info = {
            "ranking": item["rank"], 
            "uslug": item["slug"], 
            "name": item["nickname"], 
            "avatar": item["avatar"], 
            "check_in_count": item["checkin_count"]
        }
        result.append(item_info)
    return result

