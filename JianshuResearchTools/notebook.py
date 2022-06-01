from datetime import datetime
from typing import Dict, Generator, List

from .assert_funcs import AssertNotebookStatusNormal, AssertNotebookUrl
from .basic_apis import GetNotebookArticlesJsonDataApi, GetNotebookJsonDataApi

__all__ = [
    "GetNotebookName", "GetNotebookArticlesCount", "GetNotebookAuthorInfo",
    "GetNotebookWordage", "GetNotebookSubscribersCount",
    "GetNotebookUpdateTime", "GetNotebookArticlesInfo",
    "GetNotebookAllBasicData", "GetNotebookAllArticlesInfo"
]


def GetNotebookName(notebook_url: str, disable_check: bool = False) -> str:
    """获取文集名称

    Args:
        notebook_url (str): 文集 URL
        disable_check (bool): 禁用参数有效性检查. Defaults to False.

    Returns:
        str: 文集名称
    """
    if not disable_check:
        AssertNotebookUrl(notebook_url)
        AssertNotebookStatusNormal(notebook_url)
    json_obj = GetNotebookJsonDataApi(notebook_url)
    result = json_obj["name"]
    return result


def GetNotebookArticlesCount(notebook_url: str, disable_check: bool = False) -> int:
    """获取文集中的文章数量

    Args:
        notebook_url (str): 文集 URL
        disable_check (bool): 禁用参数有效性检查. Defaults to False.

    Returns:
        int: 文章数量
    """
    if not disable_check:
        AssertNotebookUrl(notebook_url)
        AssertNotebookStatusNormal(notebook_url)
    json_obj = GetNotebookJsonDataApi(notebook_url)
    result = json_obj["notes_count"]
    return result


def GetNotebookAuthorInfo(notebook_url: str, disable_check: bool = False) -> Dict:
    """获取文集作者的信息

    Args:
        notebook_url (str): 文集 URL
        disable_check (bool): 禁用参数有效性检查. Defaults to False.

    Returns:
        Dict: 作者信息
    """
    if not disable_check:
        AssertNotebookUrl(notebook_url)
        AssertNotebookStatusNormal(notebook_url)
    json_obj = GetNotebookJsonDataApi(notebook_url)
    result = {
        "name": json_obj["user"]["nickname"],
        "uslug": json_obj["user"]["slug"],
        "avatar_url": json_obj["user"]["avatar"]
    }
    return result


def GetNotebookWordage(notebook_url: str, disable_check: bool = False) -> int:
    """获取文集中所有文章的总字数

    Args:
        notebook_url (str): 文集 URL
        disable_check (bool): 禁用参数有效性检查. Defaults to False.

    Returns:
        int: 文集中的文章总字数
    """
    if not disable_check:
        AssertNotebookUrl(notebook_url)
        AssertNotebookStatusNormal(notebook_url)
    json_obj = GetNotebookJsonDataApi(notebook_url)
    result = json_obj["wordage"]
    return result


def GetNotebookSubscribersCount(notebook_url: str, disable_check: bool = False) -> int:
    """获取文集的订阅者数量

    Args:
        notebook_url (str): 文集 URL
        disable_check (bool): 禁用参数有效性检查. Defaults to False.

    Returns:
        int: 文集订阅者数量
    """
    if not disable_check:
        AssertNotebookUrl(notebook_url)
        AssertNotebookStatusNormal(notebook_url)
    json_obj = GetNotebookJsonDataApi(notebook_url)
    result = json_obj["subscribers_count"]
    return result


def GetNotebookUpdateTime(notebook_url: str, disable_check: bool = False) -> datetime:
    """获取文集的更新时间

    Args:
        notebook_url (str): 文集 URL
        disable_check (bool): 禁用参数有效性检查. Defaults to False.

    Returns:
        datetime: 更新时间
    """
    if not disable_check:
        AssertNotebookUrl(notebook_url)
        AssertNotebookStatusNormal(notebook_url)
    json_obj = GetNotebookJsonDataApi(notebook_url)
    result = datetime.fromtimestamp(json_obj["last_updated_at"])
    return result


def GetNotebookArticlesInfo(notebook_url: str, page: int = 1,
                            count: int = 10, sorting_method: str = "time",
                            disable_check: bool = False) -> List[Dict]:
    """获取文集中的文章信息

    Args:
        notebook_url (str): 文集 URL
        page (int, optional): 页码. Defaults to 1.
        count (int, optional): 每次返回的数据数量. Defaults to 10.
        sorting_method (str, optional): 排序方法，"time" 为按照发布时间排序，
        "comment_time" 为按照最近评论时间排序，"hot" 为按照热度排序. Defaults to "time".
        disable_check (bool): 禁用参数有效性检查. Defaults to False.

    Returns:
        List[Dict]: 文章信息
    """
    if not disable_check:
        AssertNotebookUrl(notebook_url)
        AssertNotebookStatusNormal(notebook_url)
    order_by = {
        "time": "added_at",
        "comment_time": "commented_at",
        "hot": "top"
    }[sorting_method]
    json_obj = GetNotebookArticlesJsonDataApi(notebook_url=notebook_url,
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


def GetNotebookAllBasicData(notebook_url: str, disable_check: bool = False) -> Dict:
    """获取文集的所有基础信息

    Args:
        notebook_url (str): 文集 URL
        disable_check (bool): 禁用参数有效性检查. Defaults to False.

    Returns:
        Dict: 文集基础信息
    """
    if not disable_check:
        AssertNotebookUrl(notebook_url)
        AssertNotebookStatusNormal(notebook_url)
    result = {}
    json_obj = GetNotebookJsonDataApi(notebook_url)

    result["name"] = json_obj["name"]
    result["author_info"] = {
        "name": json_obj["user"]["nickname"],
        "uslug": json_obj["user"]["slug"],
        "avatar_url": json_obj["user"]["avatar"]
    }
    result["articles_count"] = json_obj["notes_count"]
    result["wordage"] = json_obj["wordage"]
    result["subscribers_count"] = json_obj["subscribers_count"]
    result["update_time"] = datetime.fromtimestamp(json_obj["last_updated_at"])
    return result


def GetNotebookAllArticlesInfo(notebook_url: str, count: int = 10, sorting_method: str = "time",
                               max_count: int = None, disable_check: bool = False) -> Generator[Dict, None, None]:
    """获取文集中的全部文章信息

    Args:
        notebook_url (str): 文集 URL
        count (int, optional): 单次获取的数据数量，会影响性能. Defaults to 10.
        sorting_method (str, optional): 排序方法，time 为按照发布时间排序，
        comment_time 为按照最近评论时间排序，hot 为按照热度排序. Defaults to "time".
        max_count (int, optional): 获取的文集文章信息数量上限，Defaults to None.
        disable_check (bool): 禁用参数有效性检查. Defaults to False.

    Yields:
        Iterator[Dict], None, None]: 文章信息
    """
    if not disable_check:
        AssertNotebookUrl(notebook_url)
        AssertNotebookStatusNormal(notebook_url)
    page = 1
    now_count = 0
    while True:
        result = GetNotebookArticlesInfo(notebook_url, page, count, sorting_method, disable_check=True)
        if result:
            page += 1
        else:
            return
        for item in result:
            yield item
            if max_count:
                now_count += 1
                if max_count == now_count:
                    return
