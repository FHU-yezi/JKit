from datetime import datetime
from typing import Dict, Generator, List

from .assert_funcs import AssertCollectionStatusNormal, AssertCollectionUrl
from .basic_apis import (GetCollectionArticlesJsonDataApi,
                         GetCollectionEditorsJsonDataApi,
                         GetCollectionJsonDataApi,
                         GetCollectionRecommendedWritersJsonDataApi,
                         GetCollectionSubscribersJsonDataApi)
from .convert import CollectionUrlToCollectionSlug


def GetCollectionName(collection_url: str) -> str:
    """获取专题名称

    Args:
        collection_url (str): 专题 Url

    Returns:
        str: 专题名称
    """
    AssertCollectionUrl(collection_url)
    AssertCollectionStatusNormal(collection_url)
    json_obj = GetCollectionJsonDataApi(collection_url)
    result = json_obj["title"]
    return result


def GetCollectionAvatarUrl(collection_url: str) -> str:
    """获取专题头像链接

    Args:
        collection_url (str): 专题 Url

    Returns:
        str: 专题头像链接
    """
    AssertCollectionUrl(collection_url)
    AssertCollectionStatusNormal(collection_url)
    json_obj = GetCollectionJsonDataApi(collection_url)
    result = json_obj["image"]
    return result


def GetCollectionIntroductionText(collection_url: str) -> str:
    """获取纯文本格式的专题简介

    Args:
        collection_url (str): 专题 Url

    Returns:
        str: 纯文本格式的专题简介
    """
    AssertCollectionUrl(collection_url)
    AssertCollectionStatusNormal(collection_url)
    json_obj = GetCollectionJsonDataApi(collection_url)
    result = json_obj["content_without_html"]
    return result


def GetCollectionIntroductionHtml(collection_url: str) -> str:
    """获取 Html 格式的专题简介

    Args:
        collection_url (str): 专题 Url

    Returns:
        str: Html 格式的专题简介
    """
    AssertCollectionUrl(collection_url)
    AssertCollectionStatusNormal(collection_url)
    json_obj = GetCollectionJsonDataApi(collection_url)
    result = json_obj["content_in_full"]
    return result


def GetCollectionArticlesCount(collection_url: str) -> int:
    """获取专题中的文章数量

    Args:
        collection_url (str): 专题 Url

    Returns:
        int: 专题中的文章数量
    """
    AssertCollectionUrl(collection_url)
    AssertCollectionStatusNormal(collection_url)
    json_obj = GetCollectionJsonDataApi(collection_url)
    result = json_obj["notes_count"]
    return result


def GetCollectionSubscribersCount(collection_url: str) -> int:
    """获取专题的订阅者数量

    Args:
        collection_url (str): 专题 Url

    Returns:
        int: 专题的订阅者数量
    """
    AssertCollectionUrl(collection_url)
    AssertCollectionStatusNormal(collection_url)
    json_obj = GetCollectionJsonDataApi(collection_url)
    result = json_obj["subscribers_count"]
    return result


def GetCollectionArticlesUpdateTime(collection_url: str) -> datetime:
    """获取专题文章更新时间

    Args:
        collection_url (str): 专题 Url

    Returns:
        datetime: 专题文章更新时间
    """
    AssertCollectionUrl(collection_url)
    AssertCollectionStatusNormal(collection_url)
    json_obj = GetCollectionJsonDataApi(collection_url)
    result = datetime.fromtimestamp(json_obj["newly_added_at"])
    return result


def GetCollectionInformationUpdateTime(collection_url: str) -> datetime:
    """获取专题信息更新时间

    Args:
        collection_url (str): 专题 Url

    Returns:
        datetime: 专题信息更新时间
    """
    AssertCollectionUrl(collection_url)
    AssertCollectionStatusNormal(collection_url)
    json_obj = GetCollectionJsonDataApi(collection_url)
    result = datetime.fromtimestamp(json_obj["last_updated_at"])
    return result


def GetCollectionOwnerInfo(collection_url: str) -> Dict:
    """获取专题的所有者信息

    Args:
        collection_url (str): 专题 Url

    Returns:
        Dict: 用户信息
    """
    AssertCollectionUrl(collection_url)
    AssertCollectionStatusNormal(collection_url)
    json_obj = GetCollectionJsonDataApi(collection_url)
    result = {
        "uid": json_obj["owner"]["id"],
        "name": json_obj["owner"]["nickname"],
        "uslug": json_obj["owner"]["slug"]
    }
    return result


def GetCollectionEditorsInfo(collection_id: int, page: int = 1) -> List[Dict]:
    """获取专题编辑信息

    Args:
        collection_id (int): 专题 ID
        page (int, optional): 页码. Defaults to 1.

    Returns:
        List[Dict]: 专题编辑信息
    """
    json_obj = GetCollectionEditorsJsonDataApi(collection_id, page=page)
    result = []
    for item in json_obj["editors"]:
        item_data = {
            "uslug": item["slug"],
            "name": item["nickname"],
            "avatar_url": item["avatar_source"]
        }
        result.append(item_data)
    return result


def GetCollectionRecommendedWritersInfo(collection_id: int, page: int = 1, count: int = 20) -> List[Dict]:
    """获取专题推荐作者信息

    Args:
        collection_id (int): 专题 ID
        page (int, optional): 页码. Defaults to 1.
        count (int, optional): 每次返回的结果数量. Defaults to 20.

    Returns:
        List[Dict]: 专题推荐作者信息
    """
    json_obj = GetCollectionRecommendedWritersJsonDataApi(collection_id, page=page, count=count)
    result = []
    for item in json_obj["users"]:
        item_data = {
            "uid": item["id"],
            "uslug": item["slug"],
            "name": item["nickname"],
            "avatar_url": item["avatar_source"],
            "collection_name": item["collection_name"],
            "likes_count": item["total_likes_count"],
            "words_count": item["total_wordage"]
        }
        result.append(item_data)
    return result


def GetCollectionSubscribersInfo(collection_id: int, start_sort_id: int = None) -> List[Dict]:
    """该函数接收一个专题 ID，并返回该 ID 对应专题的关注者信息

    Args:
        collection_id (int): 专题 ID
        start_sort_id (int): 起始序号，等于上一条数据的序号

    Returns:
        List[Dict]: 关注者信息
    """
    json_obj = GetCollectionSubscribersJsonDataApi(collection_id, max_sort_id=start_sort_id)
    result = []
    for item in json_obj:
        item_data = {
            "uslug": item["slug"],
            "name": item["nickname"],
            "avatar_url": item["avatar_source"],
            "sort_id": item["like_id"],
            "subscribe_time": datetime.fromisoformat(item["subscribed_at"])
        }
        result.append(item_data)
    return result


def GetCollectionArticlesInfo(collection_url: str, page: int = 1,
                              count: int = 10, sorting_method: str = "time") -> List[Dict]:
    """该函数接收专题 Url ，并返回该 Url 对应专题的文章信息

    Args:
        collection_url (str): 专题 Url
        page (int, optional): 页码. Defaults to 1.
        count (int, optional): 每次返回的数据数量. Defaults to 10.
        sorting_method (str, optional): 排序方法，"time" 为按照发布时间排序，
        "comment_time" 为按照最近评论时间排序，"hot" 为按照热度排序. Defaults to "time".

    Returns:
        List[Dict]: 文章信息
    """
    AssertCollectionUrl(collection_url)
    AssertCollectionStatusNormal(collection_url)
    order_by = {
        "time": "added_at",
        "comment_time": "commented_at",
        "hot": "top"
    }[sorting_method]
    json_obj = GetCollectionArticlesJsonDataApi(CollectionUrlToCollectionSlug(collection_url),
                                                page=page, count=count, order_by=order_by)
    result = []
    for item in json_obj:
        item_data = {
            "aid": item["object"]["data"]["id"],
            "title": item["object"]["data"]["title"],
            "aslug": item["object"]["data"]["slug"],
            "release_time": datetime.fromisoformat(item["object"]["data"]["first_shared_at"]),
            "first_image_url": item["object"]["data"]["list_image_url"],
            "summary": item["object"]["data"]["public_abbr"],
            "views_count": item["object"]["data"]["views_count"],
            "likes_count": item["object"]["data"]["likes_count"],
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


def GetCollectionAllBasicData(collection_url: str) -> Dict:
    """获取专题的所有基础信息

    Args:
        collection_url (str): 专题 Url

    Returns:
        dict: 专题基础信息
    """
    result = {}
    json_obj = GetCollectionJsonDataApi(collection_url)

    result["name"] = json_obj["title"]
    result["avatar_url"] = json_obj["image"]
    result["introduction_text"] = json_obj["content_without_html"]
    result["introduction_html"] = json_obj["content_in_full"]
    result["articles_count"] = json_obj["notes_count"]
    result["subscribers_count"] = json_obj["subscribers_count"]
    result["articles_update_time"] = datetime.fromtimestamp(json_obj["newly_added_at"])
    result["information_update_time"] = datetime.fromtimestamp(json_obj["last_updated_at"])
    result["owner_info"] = {
        "uid": json_obj["owner"]["id"],
        "name": json_obj["owner"]["nickname"],
        "uslug": json_obj["owner"]["slug"]
    }
    return result


def GetCollectionAllEditorsInfo(collection_id: int) -> Generator[List[Dict], None, None]:
    """获取专题的所有编辑信息

    Args:
        collection_id (int): 专题 ID

    Yields:
        Iterator[List[Dict], None, None]: 当前页编辑信息
    """
    page = 1
    while True:
        result = GetCollectionEditorsInfo(collection_id, page)
        if result:
            yield result
            page += 1
        else:
            break


def GetCollectionAllRecommendedWritersInfo(collection_id: int, count: int = 20) -> Generator[List[Dict], None, None]:
    """获取专题的所有推荐作者信息

    Args:
        collection_id (int): 专题 ID
        count (int, optional): 单次获取的数据数量，会影响性能. Defaults to 20.

    Yields:
        Iterator[List[Dict], None, None]: 当前页推荐作者信息
    """
    page = 1
    while True:
        result = GetCollectionRecommendedWritersInfo(collection_id)
        if result:
            yield result
            page += 1
        else:
            break


def GetCollectionAllSubscribersInfo(collection_id: int) -> Generator[List[Dict], None, None]:
    """获取专题的所有关注者信息

    Args:
        collection_id (int): 专题 ID

    Yields:
        Iterator[List[Dict], None, None]: 当前页关注者信息
    """
    start_sort_id = None
    while True:
        result = GetCollectionSubscribersInfo(collection_id, start_sort_id)
        if result:
            yield result
            start_sort_id = result[-1]["sort_id"]
        else:
            break


def GetCollectionAllArticlesInfo(collection_url: str, count: int = 10,
                                 sorting_method: str = "time") -> Generator[List[Dict], None, None]:
    """获取专题的所有文章信息

    Args:
        collection_url (str): 专题 Url
        count (int, optional): 单次获取的数据数量，会影响性能. Defaults to 10.
        sorting_method (str, optional): 排序方法，"time" 为按照发布时间排序，
        "comment_time" 为按照最近评论时间排序，"hot" 为按照热度排序. Defaults to "time".

    Yields:
        Iterator[List[Dict], None, None]: 当前页文章信息
    """
    page = 1
    while True:
        result = GetCollectionArticlesInfo(collection_url, page, count, sorting_method)
        if result:
            yield result
            page += 1
        else:
            break
