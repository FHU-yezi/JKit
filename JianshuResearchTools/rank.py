from datetime import datetime, timedelta
from typing import Dict, List

from .basic_apis import (GetArticlesFPRankListJsonDataApi,
                         GetAssetsRankJsonDataApi,
                         GetDailyArticleRankListJsonDataApi)
from .convert import UserSlugToUserUrl
from .exceptions import APIError, ResourceError
from .user import GetUserAssetsCount


def GetAssetsRankData(start_id: int = 1, get_full: bool = False) -> List[Dict]:
    """获取资产排行榜信息

    Args:
        start_id (int, optional): 起始位置. Defaults to 1.
        get_full (bool, optional): 为 True 时获取简书贝和总资产数据. Defaults to False.

    Returns:
        List[Dict]: 资产排行榜信息
    """
    since_id = start_id - 1  # 索引下标为 0
    json_obj = GetAssetsRankJsonDataApi(max_id=1000000000, since_id=since_id)
    result = []
    for item in json_obj["rankings"]:
        item_data = {
            "ranking": item["ranking"],
            "uid": item["user"]["id"],
            "uslug": item["user"]["slug"],
            "name": item["user"]["nickname"],
            "avatar_url": item["user"]["avatar"],
            "FP": item["amount"] / 1000
        }
        if get_full:
            user_url = UserSlugToUserUrl(item_data["uslug"])
            try:
                item_data["Assets"] = GetUserAssetsCount(user_url, disable_check=True)
                item_data["FTN"] = round(item_data["Assets"] - item_data["FP"], 3)  # 处理浮点数精度问题
            except APIError:
                pass
        result.append(item_data)
    return result


def GetDailyArticleRankData() -> List[Dict]:
    """获取日更排行榜信息

    Returns:
        List[Dict]: 日更排行榜信息
    """
    json_obj = GetDailyArticleRankListJsonDataApi()
    result = []
    for item in json_obj["daps"]:
        item_data = {
            "ranking": item["rank"],
            "uslug": item["slug"],
            "name": item["nickname"],
            "avatar_url": item["avatar"],
            "check_in_count": item["checkin_count"]
        }
        result.append(item_data)
    return result


def GetArticleFPRankData(date: str = "latest") -> List[Dict]:
    """获取文章收益排行榜信息

    目前只能获取 2020 年 6 月 20 日之后的数据。

    Args:
        date (str, optional): 日期，格式“YYYYMMDD”. Defaults to "latest".

    Raises:
        ResourceError: 对应日期的排行榜数据为空时抛出此异常

    Returns:
        List[Dict]: 文章收益排行榜信息
    """
    if date == "latest":
        date = (datetime.today() + timedelta(days=-1)).strftime(r"%Y%m%d")
    json_obj = GetArticlesFPRankListJsonDataApi(date=date, type_=None)
    if json_obj["notes"] == []:
        raise ResourceError("对应日期的排行榜数据为空")
    result = []
    for ranking, item in enumerate(json_obj["notes"]):
        item_data = {
            "ranking": ranking + 1,
            "aslug": item["slug"],
            "title": item["title"],
            "author_name": item["author_nickname"],
            "author_avatar_url": item["author_avatar"],
            "fp_to_author": item["author_fp"] / 1000,
            "fp_to_voter": item["voter_fp"] / 1000,
            "total_fp": item["fp"] / 1000
        }
        result.append(item_data)
    return result


def GetArticleFPRankBasicInfo(date: str = "latest") -> Dict:
    """获取文章收益排行榜信息

    目前只能获取 2020 年 6 月 20 日之后的数据。

    Args:
        date (str, optional): 日期，格式“YYYYMMDD”. Defaults to "latest".

    Raises:
        ResourceError: 对应日期的排行榜数据为空时抛出此异常

    Returns:
        Dict: 文章收益排行榜基础信息
    """
    if date == "latest":
        date = (datetime.date.today() + datetime.timedelta(days=-1)).strftime("%Y%m%d")
    json_obj = GetArticlesFPRankListJsonDataApi(date=date, type_=None)
    if json_obj["notes"] == []:
        raise ResourceError("对应日期的排行榜数据为空")
    result = {
        "total_fp": json_obj["fp"],
        "fp_to_author": json_obj["author_fp"],
        "fp_to_voter": json_obj["voter_fp"]
    }
    return result


def GetUserFPRankData(date: str = "latest", rank_type: str = "all") -> List[Dict]:
    """获取用户收益排行榜信息

    目前只能获取 2020 年 6 月 20 日之后的数据。

    Args:
        date (str, optional): 日期，格式“YYYYMMDD”. Defaults to "latest".

    Raises:
        ResourceError: 对应日期的排行榜数据为空时抛出此异常

    Returns:
        List[Dict]: 用户收益排行榜信息
    """
    type_ = {
        "all": None,
        "write": "note",
        "vote": "like"
    }[rank_type]
    json_obj = GetArticlesFPRankListJsonDataApi(date=date, type_=type_)
    if json_obj["users"] == []:
        raise ResourceError("对应日期的排行榜数据为空")
    result = []
    for ranking, item in enumerate(json_obj["users"]):
        item_data = {
            "ranking": ranking,
            "uslug": item["slug"],
            "name": item["nickname"],
            "avatar_url": item["avatar"],
            "fp_from_write": item["author_fp"],
            "fp_from_vote": item["voter_fp"]
        }
        result.append(item_data)
    return result
