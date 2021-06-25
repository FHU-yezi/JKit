import requests
import json
from assert_funcs import AssertJianshuUrl
from basic import jianshu_request_header
from convert import UserSlugToUserUrl
from user import GetUserAssetsCount
from exceptions import APIException

def GetAssetsRankData(start_id: int =1, get_full: bool =False) -> list:
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

