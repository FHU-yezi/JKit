import json
import re
from datetime import datetime

import requests

from assert_funcs import AssertCollectionUrl
from convert import CollectionUrlToCollectionSlug
from headers import PC_header, jianshu_request_header


def GetCollectionName(collection_url: str) -> str:
    """该函数接收专题 Url，并返回该链接对应专题的名称

    Args:
        collection_url (str): 专题 Url

    Returns:
        str: 链接对应专题的名称
    """
    AssertCollectionUrl(collection_url)
    request_url = collection_url.replace("https://www.jianshu.com/c/", "https://www.jianshu.com/asimov/collections/slug/")
    source = requests.get(request_url, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    result = json_obj["title"]
    return result

def GetCollectionImageUrl(collection_url: str) -> str:
    """获取专题图片链接

    Args:
        collection_url (str): 专题 Url

    Returns:
        str: 专题图片链接
    """
    AssertCollectionUrl(collection_url)
    request_url = collection_url.replace("https://www.jianshu.com/c/", "https://www.jianshu.com/asimov/collections/slug/")
    source = requests.get(request_url, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    result = json_obj["image"]
    return result

def GetCollectionIntroductionText(collection_url: str) -> str:
    """该函数接收专题 Url，并返回该链接对应专题的简介

    Args:
        collection_url (str): 专题 Url

    Returns:
        str: 链接对应专题的简介
    """
    AssertCollectionUrl(collection_url)
    request_url = collection_url.replace("https://www.jianshu.com/c/", "https://www.jianshu.com/asimov/collections/slug/")
    source = requests.get(request_url, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    result = json_obj["content_without_html"]
    return result

def GetCollectionIntroductionHtml(collection_url: str) -> str:
    """该函数接收专题 Url，并返回该链接对应专题的简介

    Args:
        collection_url (str): 专题 Url

    Returns:
        str: 链接对应专题的简介
    """
    AssertCollectionUrl(collection_url)
    request_url = collection_url.replace("https://www.jianshu.com/c/", "https://www.jianshu.com/asimov/collections/slug/")
    source = requests.get(request_url, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    result = json_obj["content_in_full"]
    return result

def GetCollectionArticlesCount(collection_url: str) -> int:
    """该函数接收专题 Url，并返回该链接对应专题的收录文章数量

    Args:
        collection_url (str): 专题 Url

    Returns:
        int: 链接对应专题的收录文章数量
    """
    AssertCollectionUrl(collection_url)
    request_url = collection_url.replace("https://www.jianshu.com/c/", "https://www.jianshu.com/asimov/collections/slug/")
    source = requests.get(request_url, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    result = json_obj["notes_count"]
    return result

def GetCollectionSubscribersCount(collection_url: str) -> int:
    """该函数接收专题 Url，并返回该链接对应专题的关注者数量

    Args:
        collection_url (str): 专题 Url

    Returns:
        int: 链接对应专题的关注者数量
    """
    AssertCollectionUrl(collection_url)
    request_url = collection_url.replace("https://www.jianshu.com/c/", "https://www.jianshu.com/asimov/collections/slug/")
    source = requests.get(request_url, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    result = json_obj["subscribers_count"]
    return result

def GetCollectionUpdateTime(collection_url: str) -> datetime:
    """获取专题文章更新时间

    Args:
        collection_url (str): 专题 Url

    Returns:
        datetime: 专题文章更新时间
    """
    AssertCollectionUrl(collection_url)
    request_url = collection_url.replace("https://www.jianshu.com/c/", "https://www.jianshu.com/asimov/collections/slug/")
    source = requests.get(request_url, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    result = datetime.fromtimestamp(json_obj["newly_added_at"])
    return result

def GetCollectionInfoUpdatetime(collection_url: str) -> datetime:
    """获取专题信息更新时间

    Args:
        collection_url (str): 专题 Url

    Returns:
        datetime: 专题信息更新时间
    """
    AssertCollectionUrl(collection_url)
    request_url = collection_url.replace("https://www.jianshu.com/c/", "https://www.jianshu.com/asimov/collections/slug/")
    source = requests.get(request_url, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    result = datetime.fromtimestamp(json_obj["last_updated_at"])
    return result

def GetCollectionOwnerInfo(collection_url: str) -> dict:
    """获取专题的所有者信息

    Args:
        collection_url (str): 专题 Url

    Returns:
        dict: 用户信息
    """
    AssertCollectionUrl(collection_url)
    request_url = collection_url.replace("https://www.jianshu.com/c/", "https://www.jianshu.com/asimov/collections/slug/")
    source = requests.get(request_url, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    result = {
        "uid": json_obj["owner"]["id"], 
        "name": json_obj["owner"]["nickname"], 
        "uslug": json_obj["owner"]["slug"]
    }
    return result

def GetCollectionEditorsInfo(collection_id: int, page: int = 1) -> list:
    """该函数接收专题 ID，并返回 ID 对应专题的编辑信息

    Args:
        collection_id (int): 专题 ID
        page (int, optional): 页码. Defaults to 1.

    Returns:
        list: ID 对应专题的编辑信息
    """
    request_url = "https://www.jianshu.com/collections/" + str(collection_id) + "/editors"
    params = {
        "page": page
    }
    source = requests.get(request_url, params=params, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    result = []
    for item in json_obj["editors"]:
        item_data = {
            "uslug": item["slug"], 
            "name": item["nickname"], 
            "avatar": item["avatar_source"]
        }
        result.append(item_data)
    return result

def GetCollectionRecommendedWritersInfo(collection_id: int, page: int = 1, count: int = 20) -> list:
    """该函数接收一个专题 ID，并返回该 ID 对应专题的推荐作者信息

    Args:
        collection_id (int): 专题 ID
        page (int, optional): 页码. Defaults to 1.
        count (int, optional): 每次返回的数量. Defaults to 20.

    Returns:
        list: 推荐作者信息
    """
    params = {
        "collection_ids": collection_id, 
        "page": page, 
        "count": count
    }
    source = requests.get("https://www.jianshu.com/collections/recommended_users", 
                            params=params, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    result = []
    for item in json_obj["users"]:
        item_data = {
            "uid": item["id"], 
            "uslug": item["slug"], 
            "name": item["nickname"], 
            "avatar": item["avatar_source"], 
            "collection_name": item["collection_name"], 
            "likes_count": item["total_likes_count"], 
            "words_count": item["total_wordage"]
        }
        result.append(item_data)
    return result

def GetCollectionSubscribersInfo(collection_id: int, start_sort_id: int) -> list:
    """该函数接收一个专题 ID，并返回该 ID 对应专题的关注者信息

    Args:
        collection_id (int): 专题 ID
        start_sort_id (int): 起始序号，等于上一条数据的序号

    Returns:
        list: 关注者信息
    """
    request_url = "https://www.jianshu.com/collection/" + str(collection_id) + "/subscribers"
    params = {
        "max_sort_id": start_sort_id
    }
    source = requests.get(request_url, params=params, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    result = []
    for item in json_obj:
        item_data = {
            "uslug": item["slug"], 
            "name": item["nickname"], 
            "avatar": item["avatar_source"], 
            "sort_id": item["like_id"], 
            "subscribe_time": datetime.fromisoformat(item["subscribed_at"])
        }
        result.append(item_data)
    return result

def GetCollectionArticlesInfo(collection_url: str, page: int = 1, 
                                count: int = 10, sorting_method: str ="time") -> list:
    """该函数接收专题 Url ，并返回该 Url 对应专题的文章信息

    Args:
        collection_url (str): 专题 Url
        page (int, optional): 页码. Defaults to 1.
        count (int, optional): 每次返回的数据数量. Defaults to 10.
        sorting_method (str, optional): 排序方法，time 为按照发布时间排序，
        comment_time 为按照最近评论时间排序，hot 为按照热度排序. Defaults to "time".

    Returns:
        list: 文章信息
    """
    AssertCollectionUrl(collection_url)
    request_url = "https://www.jianshu.com/asimov/collections/slug/" + \
        CollectionUrlToCollectionSlug(collection_url) + "/public_notes"
    params = {
        "page": page, 
        "count": count, 
        "order_by": {
            "time": "added_at", 
            "comment_time": "commented_at", 
            "hot": "top"  # TODO: 是不是太直白了点
        }[sorting_method]
    }
    source = requests.get(request_url, params=params, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    result = []
    for item in json_obj:
        item_data  = {
            "aid": item["object"]["data"]["id"], 
            "title": item["object"]["data"]["title"], 
            "aslug": item["object"]["data"]["slug"], 
            "release_time": datetime.fromisoformat(item["object"]["data"]["first_shared_at"]), 
            "image_url": item["object"]["data"]["list_image_url"],   # TODO: 名字不太贴切
            "summary": item["object"]["data"]["public_abbr"], 
            "views_count": item["object"]["data"]["views_count"], 
            "likes_count": item["object"]["data"]["likes_count"], 
            "paid": item["object"]["data"]["paid"], 
            "commentable": item["object"]["data"]["commentable"], 
            "user": {
                "uid": item["object"]["data"]["user"]["id"], 
                "name": item["object"]["data"]["user"]["nickname"], 
                "uslug": item["object"]["data"]["user"]["slug"], 
                "avatar": item["object"]["data"]["user"]["avatar"]
            }, 
            "total_fp_amount": item["object"]["data"]["total_fp_amount"] / 1000, 
            "comments_count": item["object"]["data"]["public_comments_count"], 
            "rewards_count": item["object"]["data"]["total_rewards_count"]
        }
        result.append(item_data)
    return result
