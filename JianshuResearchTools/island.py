from datetime import datetime

from .assert_funcs import AssertIslandPostUrl, AssertIslandUrl
from .basic_apis import (GetIslandJsonDataApi, GetIslandPostJsonDataApi,
                         GetIslandPostsJsonDataApi)
from .convert import (IslandPostSlugToIslandPostUrl,
                      IslandPostUrlToIslandPostSlug, IslandUrlToIslandSlug)


def GetIslandName(island_url: str) -> str:
    """获取小岛名称

    Args:
        island_url (str): 小岛 Url

    Returns:
        str: 小岛名称
    """
    AssertIslandUrl(island_url)
    json_obj = GetIslandJsonDataApi(island_url)
    result = json_obj["name"]
    return result

def GetIslandAvatarUrl(island_url: str) -> str:
    """获取小岛头像链接

    Args:
        island_url (str): 小岛 Url

    Returns:
        str: 小岛头像链接
    """
    AssertIslandUrl(island_url)
    json_obj = GetIslandJsonDataApi(island_url)
    result = json_obj["image"]
    return result

def GetIslandIntroduction(island_url: str) -> str:
    """获取小岛简介

    Args:
        island_url (str): 小岛 Url

    Returns:
        str: 小岛简介
    """
    AssertIslandUrl(island_url)
    json_obj = GetIslandJsonDataApi(island_url)
    result = json_obj["intro"]
    return result

def GetIslandMembersCount(island_url: str) -> int:
    """获取小岛成员数量

    Args:
        island_url (str): 小岛 Url

    Returns:
        int: 成员数量
    """
    AssertIslandUrl(island_url)
    json_obj = GetIslandJsonDataApi(island_url)
    result = json_obj["members_count"]
    return result

def GetIslandPostsCount(island_url: str) -> int:
    """获取小岛帖子数量

    Args:
        island_url (str): 小岛 Url

    Returns:
        int: 帖子数量
    """
    AssertIslandUrl(island_url)
    json_obj = GetIslandJsonDataApi(island_url)
    result = json_obj["posts_count"]
    return result

def GetIslandCategory(island_url: str) -> str:
    """获取小岛分类

    Args:
        island_url (str): 小岛 Url

    Returns:
        str: 分类
    """
    AssertIslandUrl(island_url)
    json_obj = GetIslandJsonDataApi(island_url)
    result = json_obj["category"]["name"]
    return result

def GetIslandPostFullConetnt(post_url: str) -> str:
    """获取小岛帖子完整内容

    Args:
        island_url (str): 小岛 Url

    Returns:
        str: 小岛帖子完整内容
    """
    AssertIslandPostUrl(post_url)
    json_obj = GetIslandPostJsonDataApi(IslandPostUrlToIslandPostSlug(post_url))
    result = json_obj["content"]
    return result
    
def GetIslandPosts(island_url: str, start_sort_id: int = None, count: int = 10, 
                    topic_id: int = None, sorting_method: str = "time", get_full_content: bool = False) -> list:
    """获取小岛帖子信息

        Args:
            island_url (str): 小岛 Url
            start_sort_id (int, optional): 起始序号，等于上一条数据的序号. Defaults to None.
            count (int, optional): 每次返回的数据数量. Defaults to 10.
            topic_id (int, optional): 话题 ID. Defaults to None.
            sorting_method (str, optional): 排序方法，time 为按照发布时间排序，
        comment_time 为按照最近评论时间排序，hot 为按照热度排序. Defaults to "time".
            get_full_content (bool, optional): 为 True 时，当检测到获取的帖子内容不全时，
        自动调用 GetIslandPostFullConetnt 函数获取完整内容并返回. Defaults to False.

        Returns:
            list: 帖子信息
    """
    AssertIslandUrl(island_url)
    order_by = {
        "time": "latest", 
        "hot": "hot", 
        "most_valuable": "best"
    }[sorting_method], 
    json_obj = GetIslandPostsJsonDataApi(group_slug=IslandUrlToIslandSlug(island_url), 
                                      max_id=start_sort_id, count=count, topic_id=topic_id, order_by=order_by)

    result = []
    for item in json_obj:
        item_data = {
            "sorted_id": item["sorted_id"], 
            "pid": item["id"], 
            "pslug": item["slug"], 
            "title": item["title"], 
            "content": item["content"], 
            # "images": item["images"]
            "likes_count": item["likes_count"], 
            "comments_count": item["comments_count"], 
            "release_time": datetime.fromtimestamp(item["created_at"]), 
            "is_hot": item["is_hot"], 
            "is_most_valuable": item["is_best"], 
            "is_topped": item["is_top"], 
            "is_new": item["is_new"], 
            "island": {
                "iid": item["group"]["id"], 
                "islug": item["group"]["slug"], 
                "island_name": item["group"]["name"]
            }, 
            "user": {
                "uid": item["user"]["id"], 
                "uslug": item["user"]["slug"], 
                "user_name": item["user"]["nickname"], 
                "avatar_url": item["user"]["avatar"]
                # "badge": item["user"]["badge"]["text"]
                # 有个 member 不知道干什么用的，没解析
            }
            # "topic": {
            #     "tid": item["topic"]["id"], 
            #     "tslug": item["topic"]["slug"], 
            #     "topic_name": item["topic"]["name"]
            #     # 有个 group_role 不知道干什么用的，没解析
            # }
        }
        try:
            image_urls = []
            for image in item["images"]:
                image_urls.append(image["url"])
        except KeyError:
            pass  # 没有图片则跳过
        try: 
            item_data["user"]["badge"] = item["user"]["badge"]["text"]
        except KeyError:
            pass  # 没有徽章则跳过
        try:
            item_data["topic"] = {
                "tid": item["topic"]["id"], 
                "tslug": item["topic"]["slug"], 
                "topic_name": item["topic"]["name"]
                # 有个 group_role 不知道干什么用的，没解析
            }
        except KeyError:
            pass  # 没有话题则跳过
        if get_full_content and "..." in item_data["content"]:  # 获取到的帖子内容不全
            item_data["content"] = GetIslandPostFullConetnt(IslandPostSlugToIslandPostUrl(item_data["pslug"]))
        result.append(item_data)
    return result

def GetIslandAllBasicData(island_url: str) -> dict:
    """获取小岛的所有基础信息

    Args:
        island_url (str): 小岛 Url

    Returns:
        dict: 小岛基础信息
    """
    result = {}
    json_obj = GetIslandJsonDataApi(island_url)
    
    result["name"] = json_obj["name"]
    result["avatar_url"] = json_obj["image"]
    result["introduction"] = json_obj["intro"]
    result["members_count"] = json_obj["members_count"]
    result["posts_count"] = json_obj["posts_count"]
    result["category"] = json_obj["category"]["name"]
    return result

def GetIslandAllPostsData(island_url: str, count: int = 10, 
                          topic_id: int = None, sorting_method: str = "time", 
                          get_full_content: bool = False) -> list:
    """获取小岛的所有帖子信息

    Args:
        island_url (str): 小岛 Url
        count (int, optional): 单次获取的数据数量，会影响性能. Defaults to 10.
        topic_id (int, optional): 话题 ID. Defaults to None.
        sorting_method (str, optional): 排序方法，time 为按照发布时间排序，
        comment_time 为按照最近评论时间排序，hot 为按照热度排序. Defaults to "time".
        get_full_content (bool, optional): 为 True 时，当检测到获取的帖子内容不全时，
    自动调用 GetIslandPostFullConetnt 函数获取完整内容并返回. Defaults to False.

    Returns:
        list: 小岛的所有帖子信息

    Yields:
        Iterator[list]: 当前页帖子信息
    """
    start_sort_id = None
    while True:
        result = GetIslandPosts(island_url, start_sort_id, count, topic_id, sorting_method, get_full_content)
        if result:
            yield result
            start_sort_id = result[-1]["sorted_id"]
        else:
            break
