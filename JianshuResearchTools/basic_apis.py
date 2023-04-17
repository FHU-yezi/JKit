from typing import Dict, Optional

from lxml import etree
from lxml.etree import _Element

from .httpx_client import (
    JIANSHU_API_CLIENT,
    JIANSHU_MOBILE_CLIENT,
    JIANSHU_PC_CLIENT,
)

try:
    from ujson import loads as json_loads
except ImportError:
    from json import loads as json_loads

__all__ = [
    "GetArticleJsonDataApi",
    "GetArticleHtmlJsonDataApi",
    "GetArticleCommentsJsonDataApi",
    "GetCollectionJsonDataApi",
    "GetCollectionEditorsJsonDataApi",
    "GetCollectionRecommendedWritersJsonDataApi",
    "GetCollectionSubscribersJsonDataApi",
    "GetCollectionArticlesJsonDataApi",
    "GetIslandJsonDataApi",
    "GetIslandPostsJsonDataApi",
    "GetNotebookJsonDataApi",
    "GetDailyArticleRankListJsonDataApi",
    "GetArticlesFPRankListJsonDataApi",
    "GetUserJsonDataApi",
    "GetUserPCHtmlDataApi",
    "GetUserCollectionsAndNotebooksJsonDataApi",
    "GetUserArticlesListJsonDataApi",
    "GetUserFollowingListHtmlDataApi",
    "GetUserFollowersListHtmlDataApi",
    "GetUserNextAnniversaryDayHtmlDataApi",
    "GetIslandPostJsonDataApi",
    "GetUserTimelineHtmlDataApi",
]


def GetArticleJsonDataApi(article_url: str) -> Dict:
    request_url = article_url.replace("https://www.jianshu.com", "/asimov")
    source = JIANSHU_API_CLIENT.get(request_url).content
    return json_loads(source)


def GetArticleHtmlJsonDataApi(article_url: str) -> Dict:
    request_url = article_url.replace("https://www.jianshu.com", "")
    source = JIANSHU_PC_CLIENT.get(request_url).content
    html_obj = etree.HTML(source)  # type: ignore
    return json_loads(html_obj.xpath("//script[@id='__NEXT_DATA__']/text()")[0])


def GetArticleCommentsJsonDataApi(
    article_id: int, page: int, count: int, author_only: bool, order_by: str
) -> Dict:
    params = {
        "page": page,
        "count": count,
        "author_only": author_only,
        "order_by": order_by,
    }
    request_url = f"shakespeare/notes/{article_id}/comments"
    source = JIANSHU_API_CLIENT.get(request_url, params=params).content
    return json_loads(source)


def GetCollectionJsonDataApi(collection_url: str) -> Dict:
    request_url = collection_url.replace(
        "https://www.jianshu.com/c/", "asimov/collections/slug/"
    )
    source = JIANSHU_API_CLIENT.get(request_url).content
    return json_loads(source)


def GetCollectionEditorsJsonDataApi(collection_id: int, page: int) -> Dict:
    request_url = f"collections/{collection_id}/editors"
    params = {
        "page": page,
    }
    source = JIANSHU_API_CLIENT.get(request_url, params=params).content
    return json_loads(source)


def GetCollectionRecommendedWritersJsonDataApi(
    collection_id: int, page: int, count: int
) -> Dict:
    params = {
        "collection_id": collection_id,
        "page": page,
        "count": count,
    }
    source = JIANSHU_API_CLIENT.get(
        "/collections/recommended_users",
        params=params,
    ).content
    return json_loads(source)


def GetCollectionSubscribersJsonDataApi(
    collection_id: int, max_sort_id: Optional[int]
) -> Dict:
    request_url = f"/collection/{collection_id}/subscribers"
    params = {
        "max_sort_id": max_sort_id,
    }
    source = JIANSHU_API_CLIENT.get(request_url, params=params).content
    return json_loads(source)


def GetCollectionArticlesJsonDataApi(
    collection_slug: str, page: int, count: int, order_by: str
) -> Dict:
    request_url = f"/asimov/collections/slug/{collection_slug}/public_notes"
    params = {
        "page": page,
        "count": count,
        "order_by": order_by,
    }
    source = JIANSHU_API_CLIENT.get(request_url, params=params).content
    return json_loads(source)


def GetIslandJsonDataApi(island_url: str) -> Dict:
    request_url = island_url.replace("https://www.jianshu.com/g/", "/asimov/groups/")
    source = JIANSHU_API_CLIENT.get(request_url).content
    return json_loads(source)


def GetIslandPostsJsonDataApi(
    group_slug: str,
    max_id: Optional[int],
    count: int,
    topic_id: Optional[int],
    order_by: str,
) -> Dict:
    params = {
        "group_slug": group_slug,
        "order_by": order_by,
        "max_id": max_id,
        "count": count,
        "topic_id": topic_id,
    }
    source = JIANSHU_API_CLIENT.get(
        "/asimov/posts",
        params=params,
    ).content
    return json_loads(source)


def GetNotebookJsonDataApi(notebook_url: str) -> Dict:
    request_url = notebook_url.replace("https://www.jianshu.com/", "/asimov/")
    source = JIANSHU_API_CLIENT.get(request_url).content
    return json_loads(source)


def GetNotebookArticlesJsonDataApi(
    notebook_url: str, page: int, count: int, order_by: str
) -> Dict:
    request_url = (
        notebook_url.replace("https://www.jianshu.com/nb/", "/asimov/notebooks/")
        + "/public_notes/"
    )
    params = {
        "page": page,
        "count": count,
        "order_by": order_by,
    }
    source = JIANSHU_API_CLIENT.get(request_url, params=params).content
    return json_loads(source)


def GetAssetsRankJsonDataApi(max_id: int, since_id: int) -> Dict:
    params = {
        "max_id": max_id,
        "since_id": since_id,
    }
    source = JIANSHU_API_CLIENT.get(
        "/asimov/fp_rankings",
        params=params,
    ).content
    return json_loads(source)


def GetDailyArticleRankListJsonDataApi() -> Dict:
    source = JIANSHU_API_CLIENT.get(
        "/asimov/daily_activity_participants/rank",
    ).content
    return json_loads(source)


def GetArticlesFPRankListJsonDataApi(date: str, type_: Optional[str]) -> Dict:
    params = {
        "date": date,
        "type": type_,
    }
    source = JIANSHU_API_CLIENT.get(
        "/asimov/fp_rankings/voter_notes",
        params=params,
    ).content
    return json_loads(source)


def GetUserJsonDataApi(user_url: str) -> Dict:
    request_url = user_url.replace("https://www.jianshu.com/u/", "/asimov/users/slug/")
    source = JIANSHU_API_CLIENT.get(request_url).content
    return json_loads(source)


def GetUserPCHtmlDataApi(user_url: str) -> _Element:
    source = JIANSHU_PC_CLIENT.get(user_url).content
    return etree.HTML(source)  # type: ignore


def GetUserCollectionsAndNotebooksJsonDataApi(user_url: str, user_slug: str) -> Dict:
    request_url = (
        user_url.replace("https://www.jianshu.com/u/", "/users/")
        + "/collections_and_notebooks"
    )
    params = {
        "slug": user_slug,
    }
    source = JIANSHU_API_CLIENT.get(request_url, params=params).content
    return json_loads(source)


def GetUserArticlesListJsonDataApi(
    user_url: str, page: int, count: int, order_by: str
) -> Dict:
    request_url = (
        user_url.replace("https://www.jianshu.com/u/", "/asimov/users/slug/")
        + "/public_notes"
    )
    params = {
        "page": page,
        "count": count,
        "order_by": order_by,
    }
    source = JIANSHU_API_CLIENT.get(request_url, params=params).content
    return json_loads(source)


def GetUserFollowingListHtmlDataApi(user_url: str, page: int) -> _Element:
    request_url = (
        user_url.replace("https://www.jianshu.com/u/", "/users/") + "/following"
    )
    params = {
        "page": page,
    }
    source = JIANSHU_PC_CLIENT.get(request_url, params=params).content
    return etree.HTML(source)  # type: ignore


def GetUserFollowersListHtmlDataApi(user_url: str, page: int) -> _Element:
    request_url = (
        user_url.replace("https://www.jianshu.com/u/", "/users/") + "/followers"
    )
    params = {
        "page": page,
    }
    source = JIANSHU_PC_CLIENT.get(request_url, params=params).content
    return etree.HTML(source)  # type: ignore


def GetUserNextAnniversaryDayHtmlDataApi(user_slug: str) -> _Element:
    request_url = f"/mobile/u/{user_slug}/anniversary"
    source = JIANSHU_MOBILE_CLIENT.get(request_url).content
    return etree.HTML(source)  # type: ignore


def GetIslandPostJsonDataApi(post_slug: str) -> Dict:
    request_url = f"/asimov/posts/{post_slug}"
    source = JIANSHU_API_CLIENT.get(request_url).content
    return json_loads(source)


def GetUserTimelineHtmlDataApi(uslug: str, max_id: Optional[int]) -> _Element:
    request_url = f"/users/{uslug}/timeline"
    params = {
        "max_id": max_id,
    }
    source = JIANSHU_PC_CLIENT.get(request_url, params=params).content
    return etree.HTML(source)  # type: ignore
