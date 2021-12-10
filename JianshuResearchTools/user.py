from datetime import datetime
from re import findall
from typing import Dict, Generator, List

from lxml import etree

from .assert_funcs import AssertUserStatusNormal, AssertUserUrl
from .basic_apis import (GetUserArticlesListJsonDataApi,
                         GetUserCollectionsAndNotebooksJsonDataApi,
                         GetUserFollowersListHtmlDataApi,
                         GetUserFollowingListHtmlDataApi, GetUserJsonDataApi,
                         GetUserNextAnniversaryDayHtmlDataApi,
                         GetUserPCHtmlDataApi)
from .convert import UserUrlToUserSlug
from .exceptions import APIError


def GetUserName(user_url: str) -> str:
    """该函数接收用户个人主页 Url，并返回该链接对应用户的昵称

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        str: 用户昵称
    """
    AssertUserUrl(user_url)
    AssertUserStatusNormal(user_url)
    json_obj = GetUserJsonDataApi(user_url)
    result = json_obj["nickname"]
    return result

def GetUserGender(user_url: str) -> int:
    """该函数接收用户个人主页 Url，并返回该链接对应用户的性别

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        int: 用户性别，0 为未知，1 为男，2 为女
    """
    AssertUserUrl(user_url)
    AssertUserStatusNormal(user_url)
    json_obj = GetUserJsonDataApi(user_url)
    result = json_obj["gender"]
    if result == 3:  # 某些未设置性别的账号性别值为 3，怀疑为简书系统遗留问题
        result = 0  # 3 也代表性别未知
    return result

def GetUserFollowersCount(user_url: str) -> int:
    """该函数接收用户个人主页 Url，并返回该链接对应用户的关注数

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        int: 用户关注数
    """
    AssertUserUrl(user_url)
    AssertUserStatusNormal(user_url)
    json_obj = GetUserJsonDataApi(user_url)
    result = json_obj["following_users_count"]
    return result

def GetUserFansCount(user_url: str) -> int:
    """该函数接收用户个人主页 Url，并返回该链接对应用户的粉丝数

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        int: 用户粉丝数
    """
    AssertUserUrl(user_url)
    AssertUserStatusNormal(user_url)
    json_obj = GetUserJsonDataApi(user_url)
    result = json_obj["followers_count"]
    return result

def GetUserArticlesCount(user_url: str) -> int:
    """该函数接收用户个人主页 Url，并返回该链接对应用户的文章数

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        int: 用户文章数
    """
    AssertUserUrl(user_url)
    AssertUserStatusNormal(user_url)
    html_obj = GetUserPCHtmlDataApi(user_url)
    result = html_obj.xpath("//div[@class='info']/ul/li[3]/div[@class='meta-block']/a/p")[0].text
    result = int(result)
    return result

def GetUserWordage(user_url: str) -> int:
    """该函数接收用户个人主页 Url，并返回该链接对应用户的文章总字数

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        int: 用户文章总字数
    """
    AssertUserUrl(user_url)
    AssertUserStatusNormal(user_url)
    json_obj = GetUserJsonDataApi(user_url)
    result = json_obj["total_wordage"]
    return result

def GetUserLikesCount(user_url: str) -> int:
    """该函数接收用户个人主页 Url，并返回该链接对应用户的被喜欢数

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        int: 用户被喜欢数
    """
    AssertUserUrl(user_url)
    AssertUserStatusNormal(user_url)
    json_obj = GetUserJsonDataApi(user_url)
    result = json_obj["total_likes_count"]
    return result

def GetUserAssetsCount(user_url: str) -> float:
    """该函数接收用户个人主页 Url，并返回该链接对应用户的总资产
    
    # ! 当用户资产大于 10000 时，结果的精确度将下降到 1000

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        float: 用户总资产
    """
    AssertUserUrl(user_url)
    AssertUserStatusNormal(user_url)
    html_obj = GetUserPCHtmlDataApi(user_url)
    try:
        result = html_obj.xpath("//div[@class='info']/ul/li[6]/div[@class='meta-block']/p")[0].text
    except IndexError:
        raise APIError("受简书网页展示限制，无法获取该用户的总资产")
    result = float(result.replace(".", "").replace("w", "000"))
    return result

def GetUserFPCount(user_url: str) -> float:
    """该函数接收用户个人主页 Url，并返回该链接对应用户的简书钻数量

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        float: 用户简书钻数量
    """
    AssertUserUrl(user_url)
    AssertUserStatusNormal(user_url)
    json_obj = GetUserJsonDataApi(user_url)
    result = json_obj["jsd_balance"] / 1000
    if json_obj["total_wordage"] == 0 and result == 0:
        raise APIError("受简书限制，无法获取该用户的简书钻数量")
    return result

def GetUserFTNCount(user_url: str) -> float:
    """该函数接收用户个人主页 Url，并返回该链接对应用户的简书贝数量

    # ! 视用户资产配置情况不同，该函数获取到的数值会有不大于 1000 的偏差

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        float: 用户简书贝数量
    """
    assets = GetUserAssetsCount(user_url)
    FTN = GetUserFPCount(user_url)
    result = assets - FTN
    result = abs(result)  # 处理用户简书贝数量较少导致结果为负的情况
    result = round(result, 3)  # 处理浮点数精度问题
    return result

def GetUserBadgesList(user_url: str) -> List:
    """该函数接收用户个人主页 Url，并返回该链接对应用户的徽章列表

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        list: 用户徽章列表
    """
    AssertUserUrl(user_url)
    AssertUserStatusNormal(user_url)
    html_obj = GetUserPCHtmlDataApi(user_url)
    result = html_obj.xpath("//li[@class='badge-icon']/a/text()")
    result = [item.replace(" ", "").replace("\n", "") for item in result]  # 移除空格和换行符
    result = [item for item in result if item != ""]  # 去除空值
    return result

def GetUserLastUpdateTime(user_url: str) -> datetime:
    """该函数接收用户个人主页 Url，并返回该链接对应用户的文章最近更新时间

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        datetime: 用户文章最近更新时间
    """
    AssertUserUrl(user_url)
    AssertUserStatusNormal(user_url)
    json_obj = GetUserJsonDataApi(user_url)
    result = datetime.fromtimestamp(json_obj["last_updated_at"])
    return result

def GetUserVIPInfo(user_url: str) -> Dict:
    """该函数接收用户个人主页 Url，并返回该链接对应用户的会员信息

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        dict: 用户会员信息
    """
    AssertUserUrl(user_url)
    AssertUserStatusNormal(user_url)
    json_obj = GetUserJsonDataApi(user_url)
    try:
        result = {
            "vip_type": {
                "bronze": "铜牌",
                "silver": "银牌" , 
                "gold": "黄金", 
                "platina": "白金"
            }[json_obj["member"]["type"]], 
            "expire_date": datetime.fromtimestamp(json_obj["member"]["expires_at"])
        }
    except KeyError:
        result = {
            "vip_type": None, 
            "expire_date": None
        }
    return result

def GetUserIntroductionHtml(user_url: str) -> str:
    """该函数接收用户个人主页 Url，并返回该链接对应用户的个人简介

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        str: Html 格式的用户个人简介
    """
    AssertUserUrl(user_url)
    AssertUserStatusNormal(user_url)
    json_obj = GetUserJsonDataApi(user_url)
    result = json_obj["intro"]
    return result

def GetUserIntroductionText(user_url: str) -> str:
    """该函数接收用户个人主页 Url，并返回该链接对应用户的个人简介

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        str: 纯文本格式的用户个人简介
    """
    AssertUserUrl(user_url)
    AssertUserStatusNormal(user_url)
    json_obj = GetUserJsonDataApi(user_url)
    if json_obj["intro"] == "":   # 简介为空
        return ""
    html_obj = etree.HTML(json_obj["intro"])
    result = html_obj.xpath("//*/text()")
    result = "\n".join(result)
    return result

def GetUserNextAnniversaryDay(user_url: str) -> datetime:
    """该函数用于获取用户的下一次简书周年纪念时间

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        datetime: 下一次简书周年纪念时间
    """
    AssertUserUrl(user_url)
    AssertUserStatusNormal(user_url)
    user_slug = UserUrlToUserSlug(user_url)
    html_obj = GetUserNextAnniversaryDayHtmlDataApi(user_slug)
    result = html_obj.xpath('//*[@id="app"]/div[1]/div/text()')[0]
    result = findall(r"\d+", result)
    result = datetime.fromisoformat("-".join(result))
    return result

def GetUserNotebooksInfo(user_url: str) -> List:
    """该函数接收用户个人主页 Url，并返回该链接对应用户的文集与连载信息

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        list: 用户文集与连载信息
    """
    AssertUserUrl(user_url)
    AssertUserStatusNormal(user_url)
    json_obj = GetUserCollectionsAndNotebooksJsonDataApi(user_url=user_url, user_slug=UserUrlToUserSlug(user_url))
    result = []
    for item in json_obj["notebooks"]:
        item_data = {
            "nid": item["id"], 
            "name": item["name"], 
            "is_book": item["book"]
        }
        if item["book"] == True:
            item_data["is_paid_book"] = item["paid_book"]  # 如果是连载，则判断是否是付费连载
        result.append(item_data)
    return result

def GetUserOwnCollectionsInfo(user_url: str) -> List:
    """该函数接收用户个人主页 Url，并返回该链接对应用户自己创建的专题信息

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        list: 用户自己创建的专题信息
    """
    AssertUserUrl(user_url)
    AssertUserStatusNormal(user_url)
    json_obj = GetUserCollectionsAndNotebooksJsonDataApi(user_url=user_url, user_slug=UserUrlToUserSlug(user_url))
    result = []
    for item in json_obj["own_collections"]:
        item_data = {
            "cid": item["id"], 
            "cslug": item["slug"], 
            "name": item["title"], 
            "avatar_url": item["avatar"]
        }
        result.append(item_data)
    return result

def GetUserManageableCollectionsInfo(user_url: str) -> List:
    """该函数接收用户个人主页 Url，并返回该链接对应用户有管理权限的专题信息

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        list: 用户有管理权限的专题信息
    """
    AssertUserUrl(user_url)
    AssertUserStatusNormal(user_url)
    json_obj = GetUserCollectionsAndNotebooksJsonDataApi(user_url=user_url, user_slug=UserUrlToUserSlug(user_url))
    result = []
    for item in json_obj["manageable_collections"]:
        item_data = {
            "cid": item["id"], 
            "cslug": item["slug"], 
            "name": item["title"], 
            "avatar_url": item["avatar"]
        }
        result.append(item_data)
    return result

def GetUserArticlesInfo(user_url: str, page: int = 1, count: int = 10, 
                        sorting_method: str = "time") -> List:
    """该函数接收用户个人主页 Url，并返回该链接对应用户的文章信息

    Args:
        user_url (str): 用户个人主页 Url
        page (int, optional): 页码，与网页端文章顺序相同. Defaults to 1.
        count (int, optional): 获取的文章数量. Defaults to 10.
        sorting_method (str, optional): 排序方法，time 为按照发布时间排序，
        comment_time 为按照最近评论时间排序，hot 为按照热度排序. Defaults to "time".

    Returns:
        list: 用户文章信息
    """
    AssertUserUrl(user_url)
    AssertUserStatusNormal(user_url)
    order_by = {
        "time": "added_at", 
        "comment_time": "commented_at", 
        "hot": "top"
    }[sorting_method]
    json_obj = GetUserArticlesListJsonDataApi(user_url=user_url, page=page, 
                                           count=count, order_by=order_by)
    result = []
    for item in json_obj:
        item_data  = {
            "aid": item["object"]["data"]["id"], 
            "title": item["object"]["data"]["title"], 
            "aslug": item["object"]["data"]["slug"], 
            "release_time": datetime.fromisoformat(item["object"]["data"]["first_shared_at"]), 
            "first_image_url": item["object"]["data"]["list_image_url"], 
            "summary": item["object"]["data"]["public_abbr"], 
            "views_count": item["object"]["data"]["views_count"], 
            "likes_count": item["object"]["data"]["likes_count"], 
            "is_top": item["object"]["data"]["is_top"], 
            "paid": item["object"]["data"]["paid"], 
            "commentable": item["object"]["data"]["commentable"], 
            "user": {
                "uid": item["object"]["data"]["user"]["id"], 
                "name": item["object"]["data"]["user"]["nickname"], 
                "uslug": item["object"]["data"]["user"]["slug"], 
                "avatar_url": item["object"]["data"]["user"]["avatar"]
            }, 
            "total_fp_amount": item["object"]["data"]["total_fp_amount"] / 1000, 
            "comments_count": item["object"]["data"]["public_comments_count"], 
            "rewards_count": item["object"]["data"]["total_rewards_count"]
        }
        result.append(item_data)
    return result

def GetUserFollowingInfo(user_url: str, page:int = 1) -> List:
    """该函数接收用户个人主页 Url 和页码，并返回该用户关注列表中对应页数的用户信息

    Args:
        user_url (str): 用户个人主页 Url
        page (int, optional): 关注列表页码. Defaults to 1.

    Returns:
        list: 该用户关注列表中对应页数的用户信息
    """
    AssertUserUrl(user_url)
    AssertUserStatusNormal(user_url)
    html_obj = GetUserFollowingListHtmlDataApi(user_url=user_url, page=page)
    name_raw_data = html_obj.xpath("//a[@class='name']")[1:]
    if not name_raw_data:  # 判断该页数据是否为空
        return []
    followers_raw_data = html_obj.xpath("//div[@class='meta'][1]/span[1]")
    fans_raw_data = html_obj.xpath("//div[@class='meta'][1]/span[2]")
    articles_raw_data = html_obj.xpath("//div[@class='meta'][1]/span[3]")
    words_and_likes_raw_data = html_obj.xpath("//div[@class='meta'][2]")
    result = []
    for index in range(8):
        item_data = {
            "name": name_raw_data[index].text, 
            "followers_count": int(followers_raw_data[index].text.replace("关注 ", "")), 
            "fans_count": int(fans_raw_data[index].text.replace("粉丝", "")), 
            "articles_count": int(articles_raw_data[index].text.replace("文章 ", "")), 
            "words_count": int(findall(r"\d+", words_and_likes_raw_data[index].text)[0]),   # TODO: 重复运行正则匹配，影响效率，需要优化
            "likes_count": int(findall(r"\d+", words_and_likes_raw_data[index].text)[1])
        }
        result.append(item_data)
    return result

def GetUserFansInfo(user_url: str, page:int = 1) -> List:
    """该函数接收用户个人主页 Url 和页码，并返回该用户粉丝列表中对应页数的用户信息

    Args:
        user_url (str): 用户个人主页 Url
        page (int, optional): 粉丝列表页码. Defaults to 1.

    Returns:
        list: 该用户粉丝列表中对应页数的用户信息
    """
    AssertUserUrl(user_url)
    AssertUserStatusNormal(user_url)
    html_obj = GetUserFollowersListHtmlDataApi(user_url=user_url, page=page)
    name_raw_data = html_obj.xpath("//a[@class='name']")[1:]
    if not name_raw_data:  # 判断该页数据是否为空
        return []
    followers_raw_data = html_obj.xpath("//div[@class='meta'][1]/span[1]")
    fans_raw_data = html_obj.xpath("//div[@class='meta'][1]/span[2]")
    articles_raw_data = html_obj.xpath("//div[@class='meta'][1]/span[3]")
    words_and_likes_raw_data = html_obj.xpath("//div[@class='meta'][2]")
    result = []
    for index in range(8):
        item_data = {
            "name": name_raw_data[index].text, 
            "followers_count": int(followers_raw_data[index].text.replace("关注 ", "")), 
            "fans_count": int(fans_raw_data[index].text.replace("粉丝", "")), 
            "articles_count": int(articles_raw_data[index].text.replace("文章 ", "")), 
            "words_count": int(findall(r"\d+", words_and_likes_raw_data[index].text)[0]),   # TODO: 重复运行正则匹配，影响效率，需要优化
            "likes_count": int(findall(r"\d+", words_and_likes_raw_data[index].text)[1])
        }
        result.append(item_data)
    return result

def GetUserAllBasicData(user_url: str) -> Dict:
    """获取用户的所有基础信息

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        dict: 用户基础信息
    """
    
    result = {}
    json_obj = GetUserJsonDataApi(user_url)
    html_obj = GetUserPCHtmlDataApi(user_url)
    anniversary_day_html_obj = GetUserNextAnniversaryDayHtmlDataApi(UserUrlToUserSlug(user_url))
    
    result["name"] = json_obj["nickname"]
    result["url"] = user_url
    result["uslug"] = UserUrlToUserSlug(user_url)
    result["gender"] = json_obj["gender"]
    result["followers_count"] = json_obj["following_users_count"]
    result["fans_count"] = json_obj["followers_count"]
    result["articles_count"] = json_obj
    result["wordage"] = json_obj["total_wordage"]
    result["likes_count"] = json_obj["total_likes_count"]
    try:
        result["assets_count"] = html_obj.xpath("//div[@class='info']/ul/li[6]/div[@class='meta-block']/p")[0].text
        result["assets_count"] = float(result["assets_count"].replace(".", "").replace("w", "000"))
    except IndexError:
        result["assets_count"] = None
    if json_obj["total_wordage"] == 0 and json_obj["jsd_balance"] == 0:
        result["FP_count"] = None
    else:
        result["FP_count"] = json_obj["jsd_balance"] / 1000
    if result["assets_count"] and result["FP_count"]:
        result["FTN_count"] = result["assets_count"] - result["FP_count"]
        result["FTN_count"] = round(abs(result["FTN_count"]), 3)
    else:
        result["FTN_count"] = None
    result["badges_list"] = html_obj.xpath("//li[@class='badge-icon']/a/text()")
    result["badges_list"] = [item.replace(" ", "").replace("\n", "") for item in result["badges_list"]]  # 移除空格和换行符
    result["badges_list"] = [item for item in result["badges_list"] if item != ""]  # 去除空值
    result["last_update_time"] = datetime.fromtimestamp(json_obj["last_updated_at"])
    try:
        result["vip_info"] = {
            "vip_type": {
                    "bronze": "铜牌",
                    "silver": "银牌" , 
                    "gold": "黄金", 
                    "platina": "白金"
                }[json_obj["member"]["type"]], 
                "expire_date": datetime.fromtimestamp(json_obj["member"]["expires_at"])
            }
    except KeyError:
        result["vip_info"] = {
            "vip_type": None, 
            "expire_date": None
        }
    result["introduction_html"] = json_obj["intro"]
    if not result["introduction_html"]:
        result["introduction_text"] = ""
    else:
        result["introduction_text"] = "\n".join(etree.HTML(result["introduction_html"]).xpath("//*/text()"))
    result["next_anniversary_day"] = anniversary_day_html_obj.xpath('//*[@id="app"]/div[1]/div/text()')[0]
    result["next_anniversary_day"] = datetime.fromisoformat("-".join(findall(r"\d+", result["next_anniversary_day"])))
    return result

def GetUserAllArticlesInfo(user_url: str, count: int = 10, sorting_method: str = "time") -> Generator[List, None, None]:
    """获取用户的所有文章信息

    Args:
        user_url (str): 用户个人主页 Url
        count (int, optional): 单次获取的数据数量，会影响性能. Defaults to 10.
        sorting_method (str, optional): 排序方法，time 为按照发布时间排序，
        comment_time 为按照最近评论时间排序，hot 为按照热度排序. Defaults to "time".

    Yields:
        Iterator[List, None, None]: 当前页文章信息
    """
    page = 1
    while True:
        result = GetUserArticlesInfo(user_url, page, count, sorting_method)
        if result:
            yield result
            page += 1
        else:
            break

def GetUserAllFollowingInfo(user_url: str) -> Generator[List, None, None]:
    """获取用户的所有关注者信息

    Args:
        user_url (str): 用户个人主页 Url

    Yields:
        Iterator[List, None, None]: 当前页关注者信息
    """
    page = 1
    while True:
        result = GetUserFollowingInfo(user_url, page)
        if result:
            yield result
            page += 1
        else:
            break

def GetUserAllFansInfo(user_url: str) -> Generator[List, None, None]:
    """获取用户的所有粉丝信息

    Args:
        user_url (str): 用户个人主页 Url

    Yields:
        Iterator[List, None, None]: 当前页粉丝信息
    """
    page = 1
    while True:
        result = GetUserFansInfo(user_url, page)
        if result:
            yield result
            page += 1
        else:
            break
