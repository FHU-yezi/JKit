import json

import requests
from lxml import etree

from assert_funcs import AssertUserUrl
from convert import *
from basic import PC_header, jianshu_request_header, mobile_header
from exceptions import *


def GetUserName(user_url: str) -> str:
    """该函数接收用户个人主页 Url，并返回该链接对应用户的昵称

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        str: 用户昵称
    """
    AssertUserUrl(user_url)
    source = requests.get(user_url, headers=PC_header).content
    html_obj = etree.HTML(source)
    result = html_obj.xpath("//a[@class='name']")[0].text
    return result

def GetUserFollowersCount(user_url: str) -> int:
    """该函数接收用户个人主页 Url，并返回该链接对应用户的关注数

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        int: 用户关注数
    """
    AssertUserUrl(user_url)
    source = requests.get(user_url, headers=PC_header).content
    html_obj = etree.HTML(source)
    result = html_obj.xpath("//div[@class='info']/ul/li[1]/div[@class='meta-block']/a/p")[0].text
    result = int(result)
    return result

def GetUserFansCount(user_url: str) -> int:
    """该函数接收用户个人主页 Url，并返回该链接对应用户的粉丝数

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        int: 用户粉丝数
    """
    AssertUserUrl(user_url)
    source = requests.get(user_url, headers=PC_header).content
    html_obj = etree.HTML(source)
    result = html_obj.xpath("//div[@class='info']/ul/li[2]/div[@class='meta-block']/a/p")[0].text
    result = int(result)
    return result

def GetUserArticlesCount(user_url: str) -> int:
    """该函数接收用户个人主页 Url，并返回该链接对应用户的文章数

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        int: 用户文章数
    """
    AssertUserUrl(user_url)
    source = requests.get(user_url, headers=PC_header).content
    html_obj = etree.HTML(source)
    result = html_obj.xpath("//div[@class='info']/ul/li[3]/div[@class='meta-block']/a/p")[0].text
    result = int(result)
    return result

def GetUserWordsCount(user_url: str) -> int:
    """该函数接收用户个人主页 Url，并返回该链接对应用户的文章总字数

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        int: 用户文章总字数
    """
    AssertUserUrl(user_url)
    source = requests.get(user_url, headers=PC_header).content
    html_obj = etree.HTML(source)
    result = html_obj.xpath("//div[@class='info']/ul/li[4]/div[@class='meta-block']/p")[0].text
    result = int(result)
    return result

def GetUserLikesCount(user_url: str) -> int:
    """该函数接收用户个人主页 Url，并返回该链接对应用户的被喜欢数

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        int: 用户被喜欢数
    """
    AssertUserUrl(user_url)
    source = requests.get(user_url, headers=PC_header).content
    html_obj = etree.HTML(source)
    result = html_obj.xpath("//div[@class='info']/ul/li[5]/div[@class='meta-block']/p")[0].text
    result = int(result)
    return result

def GetUserAssetsCount(user_url: str) -> int:
    """该函数接收用户个人主页 Url，并返回该链接对应用户的总资产
    
    # ! 当用户资产大于 10000 时，结果的精确度将下降到 1000

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        int: 用户总资产
    """
    AssertUserUrl(user_url)
    source = requests.get(user_url, headers=PC_header).content
    html_obj = etree.HTML(source)
    try:
        result = html_obj.xpath("//div[@class='info']/ul/li[6]/div[@class='meta-block']/p")[0].text
    except IndexError:
        raise APIException("受简书网页展示限制，无法获取该用户的总资产")
    result = float(result.replace(".", "").replace("w", "000"))
    return result

def GetUserFP(user_url: str) -> str:
    """该函数接收用户个人主页 Url，并返回该链接对应用户的简书钻数量

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        int: 用户简书钻数量
    """
    AssertUserUrl(user_url)
    source = requests.get(user_url, headers=mobile_header).content
    html_obj = etree.HTML(source)
    try:
        result = html_obj.xpath("//div[@class='follow-meta']/span[3]")[0].text
    except IndexError:
        raise APIException("受简书网页展示限制，无法获取该用户的简书钻数量")
    result = float(result)
    return result

def GetUserBadgesList(user_url: str) -> list:
    """该函数接收用户个人主页 Url，并返回该链接对应用户的徽章列表

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        list: 用户被喜欢数
    """
    AssertUserUrl(user_url)
    source = requests.get(user_url, headers=PC_header).content
    html_obj = etree.HTML(source)
    result = html_obj.xpath("//li[@class='badge-icon']/a/text()")
    result = [item.replace(" ", "").replace("\n", "") for item in result]  # 移除空格和换行符
    result = [item for item in result if item != ""]  # 去除空值
    return result

def GetUserIntroduction(user_url: str) -> str:
    """该函数接收用户个人主页 Url，并返回该链接对应用户的个人简介

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        str: 用户个人简介
    """
    AssertUserUrl(user_url)
    source = requests.get(user_url, headers=PC_header).content
    html_obj = etree.HTML(source)
    lines = html_obj.xpath("//div[@class='js-intro']/text() | //div[@class='js-intro']/a/@href")  # 同时获取文字和链接
    result = "\n".join(lines)
    return result

def GetUserBasicInformation(user_url: str) -> dict:
    # TODO: 这个名字有点难理解，应该改个名
    """该函数接收用户个人主页 Url，并返回该链接对应用户的基础信息

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        dict: 用户基础信息
    """
    AssertUserUrl(user_url)
    source = requests.get(user_url, headers=PC_header).content
    html_obj = etree.HTML(source)
    result = {
        "name": html_obj.xpath("//a[@class='name']")[0].text, 
        "followers_count": int(html_obj.xpath("//div[@class='info']/ul/li[1]/div[@class='meta-block']/a/p")[0].text), 
        "fans_count": int(html_obj.xpath("//div[@class='info']/ul/li[2]/div[@class='meta-block']/a/p")[0].text), 
        "articles_count": int(html_obj.xpath("//div[@class='info']/ul/li[3]/div[@class='meta-block']/a/p")[0].text), 
        "words_count": int(html_obj.xpath("//div[@class='info']/ul/li[4]/div[@class='meta-block']/p")[0].text), 
        "likes_count": int(html_obj.xpath("//div[@class='info']/ul/li[5]/div[@class='meta-block']/p")[0].text)
    }
    try:  # 由于资产信息有可能出现获取失败的情况，故需要单独处理
        assets_count = html_obj.xpath("//div[@class='info']/ul/li[6]/div[@class='meta-block']/p")[0].text
    except IndexError:
        print("受简书网页展示限制，无法获取该用户的总资产。\n为保证其它数据正常获取，该错误已被屏蔽")
    else:
        assets_count = float(assets_count.replace(".", "").replace("w", "000"))
        result["assets_count"] = assets_count
    return result

def GetUserNotebooksInfo(user_url: str) -> list:
    """该函数接收用户个人主页 Url，并返回该链接对应用户的文集与连载信息

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        list: 用户文集与连载信息
    """
    AssertUserUrl(user_url)
    request_url = user_url.replace("/u/", "/users/") + "/collections_and_notebooks"
    params = {
        "slug": UserUrlToUserSlug(user_url)
    }
    source = requests.get(request_url, headers=jianshu_request_header, params=params).content
    json_obj = json.loads(source)
    result = []
    for item in json_obj["notebooks"]:
        item_info = {
            "nid": item["id"], 
            "name": item["name"], 
            "is_book": item["book"]
        }
        if item["book"] == True:
            item_info["is_paid_book"] = item["paid_book"]  # 如果是连载，则判断是否是付费连载
        result.append(item_info)
    return result

def GetUserOwnCollectionsInfo(user_url: str) -> list:
    """该函数接收用户个人主页 Url，并返回该链接对应用户自己创建的专题信息

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        list: 用户自己创建的专题信息
    """
    AssertUserUrl(user_url)
    request_url = user_url.replace("/u/", "/users/") + "/collections_and_notebooks"
    params = {
        "slug": UserUrlToUserSlug(user_url)
    }
    source = requests.get(request_url, headers=jianshu_request_header, params=params).content
    json_obj = json.loads(source)
    result = []
    for item in json_obj["own_collections"]:
        item_info = {
            "cid": item["id"], 
            "cslug": item["slug"], 
            "name": item["title"], 
            "avatar": item["avatar"]
        }
        result.append(item_info)
    return result

def GetUserManageableCollectionsInfo(user_url: str) -> list:
    """该函数接收用户个人主页 Url，并返回该链接对应用户有管理权限的专题信息

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        list: 用户有管理权限的专题信息
    """
    AssertUserUrl(user_url)
    request_url = user_url.replace("/u/", "/users/") + "/collections_and_notebooks"
    params = {
        "slug": UserUrlToUserSlug(user_url)
    }
    source = requests.get(request_url, headers=jianshu_request_header, params=params).content
    json_obj = json.loads(source)
    result = []
    for item in json_obj["manageable_collections"]:
        item_info = {
            "cid": item["id"], 
            "cslug": item["slug"], 
            "name": item["title"], 
            "avatar": item["avatar"]
        }
        result.append(item_info)
    return result