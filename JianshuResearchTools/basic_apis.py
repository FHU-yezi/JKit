from typing import Dict, Optional

from lxml import etree
from lxml.etree import _Element

from .headers import (
    PC_header,
    api_request_header,
    mobile_header,
)
from .httpx_client import client

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
    request_url = article_url.replace(
        "https://www.jianshu.com/", "https://www.jianshu.com/asimov/"
    )
    source = client.get(request_url, headers=api_request_header).content
    return json_loads(source)


def GetArticleHtmlJsonDataApi(article_url: str) -> Dict:
    source = client.get(article_url, headers=PC_header).content
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
    request_url = f"https://www.jianshu.com/shakespeare/notes/{article_id}/comments"
    source = client.get(request_url, params=params, headers=api_request_header).content
    return json_loads(source)


def GetCollectionJsonDataApi(collection_url: str) -> Dict:
    request_url = collection_url.replace(
        "https://www.jianshu.com/c/", "https://www.jianshu.com/asimov/collections/slug/"
    )
    source = client.get(request_url, headers=api_request_header).content
    return json_loads(source)


def GetCollectionEditorsJsonDataApi(collection_id: int, page: int) -> Dict:
    request_url = f"https://www.jianshu.com/collections/{collection_id}/editors"
    params = {"page": page}
    source = client.get(request_url, params=params, headers=api_request_header).content
    return json_loads(source)


def GetCollectionRecommendedWritersJsonDataApi(
    collection_id: int, page: int, count: int
) -> Dict:
    params = {"collection_id": collection_id, "page": page, "count": count}
    source = client.get(
        "https://www.jianshu.com/collections/recommended_users",
        params=params,
        headers=api_request_header,
    ).content
    return json_loads(source)


def GetCollectionSubscribersJsonDataApi(
    collection_id: int, max_sort_id: Optional[int]
) -> Dict:
    request_url = f"https://www.jianshu.com/collection/{collection_id}/subscribers"
    params = {"max_sort_id": max_sort_id}
    source = client.get(request_url, params=params, headers=api_request_header).content
    return json_loads(source)


def GetCollectionArticlesJsonDataApi(
    collection_slug: str, page: int, count: int, order_by: str
) -> Dict:
    request_url = f"https://www.jianshu.com/asimov/collections/slug/{collection_slug}/public_notes"
    params = {"page": page, "count": count, "order_by": order_by}
    source = client.get(request_url, params=params, headers=api_request_header).content
    return json_loads(source)


def GetIslandJsonDataApi(island_url: str) -> Dict:
    request_url = island_url.replace(
        "https://www.jianshu.com/g/", "https://www.jianshu.com/asimov/groups/"
    )
    source = client.get(request_url, headers=api_request_header).content
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
    source = client.get(
        "https://www.jianshu.com/asimov/posts",
        params=params,
        headers=api_request_header,
    ).content
    return json_loads(source)


def GetNotebookJsonDataApi(notebook_url: str) -> Dict:
    request_url = notebook_url.replace(
        "https://www.jianshu.com/", "https://www.jianshu.com/asimov/"
    )
    source = client.get(request_url, headers=api_request_header).content
    return json_loads(source)


def GetNotebookArticlesJsonDataApi(
    notebook_url: str, page: int, count: int, order_by: str
) -> Dict:
    request_url = (
        notebook_url.replace(
            "https://www.jianshu.com/nb/", "https://www.jianshu.com/asimov/notebooks/"
        )
        + "/public_notes/"
    )
    params = {"page": page, "count": count, "order_by": order_by}
    source = client.get(request_url, params=params, headers=api_request_header).content
    return json_loads(source)


def GetAssetsRankJsonDataApi(max_id: int, since_id: int) -> Dict:
    params = {"max_id": max_id, "since_id": since_id}
    source = client.get(
        "https://www.jianshu.com/asimov/fp_rankings",
        params=params,
        headers=api_request_header,
    ).content
    return json_loads(source)


def GetDailyArticleRankListJsonDataApi() -> Dict:
    source = client.get(
        "https://www.jianshu.com/asimov/daily_activity_participants/rank",
        headers=api_request_header,
    ).content
    return json_loads(source)


def GetArticlesFPRankListJsonDataApi(
    date: str, type_: Optional[str]
) -> Dict:  # 避免覆盖内置函数
    params = {"date": date, "type": type_}
    source = client.get(
        "https://www.jianshu.com/asimov/fp_rankings/voter_notes",
        params=params,
        headers=api_request_header,
    ).content
    return json_loads(source)


def GetUserJsonDataApi(user_url: str) -> Dict:
    request_url = user_url.replace(
        "https://www.jianshu.com/u/", "https://www.jianshu.com/asimov/users/slug/"
    )
    source = client.get(request_url, headers=api_request_header).content
    return json_loads(source)


def GetUserPCHtmlDataApi(user_url: str) -> _Element:
    source = client.get(user_url, headers=PC_header).content
    return etree.HTML(source)  # type: ignore


def GetUserCollectionsAndNotebooksJsonDataApi(user_url: str, user_slug: str) -> Dict:
    request_url = user_url.replace("/u/", "/users/") + "/collections_and_notebooks"
    params = {"slug": user_slug}
    source = client.get(request_url, headers=api_request_header, params=params).content
    return json_loads(source)


def GetUserArticlesListJsonDataApi(
    user_url: str, page: int, count: int, order_by: str
) -> Dict:
    request_url = user_url.replace("/u/", "/asimov/users/slug/") + "/public_notes"
    params = {"page": page, "count": count, "order_by": order_by}
    source = client.get(request_url, headers=api_request_header, params=params).content
    return json_loads(source)


def GetUserFollowingListHtmlDataApi(user_url: str, page: int) -> _Element:
    request_url = user_url.replace("/u/", "/users/") + "/following"
    params = {"page": page}
    source = client.get(request_url, headers=PC_header, params=params).content
    return etree.HTML(source)  # type: ignore


def GetUserFollowersListHtmlDataApi(user_url: str, page: int) -> _Element:
    request_url = user_url.replace("/u/", "/users/") + "/followers"
    params = {"page": page}
    source = client.get(request_url, headers=PC_header, params=params).content
    return etree.HTML(source)  # type: ignore


def GetUserNextAnniversaryDayHtmlDataApi(user_slug: str) -> _Element:
    request_url = f"https://www.jianshu.com/mobile/u/{user_slug}/anniversary"
    source = client.get(request_url, headers=mobile_header).content
    return etree.HTML(source)  # type: ignore


def GetIslandPostJsonDataApi(post_slug: str) -> Dict:
    request_url = f"https://www.jianshu.com/asimov/posts/{post_slug}"
    source = client.get(request_url, headers=api_request_header).content
    return json_loads(source)


def GetUserTimelineHtmlDataApi(uslug: str, max_id: Optional[int]) -> _Element:
    request_url = f"https://www.jianshu.com/users/{uslug}/timeline"
    params = {"max_id": max_id}
    source = client.get(request_url, headers=PC_header, params=params).content
    return etree.HTML(source)  # type: ignore
