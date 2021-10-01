from datetime import datetime

import requests
from lxml import etree

from .headers import *

try:
    import simplejson as json
except ImportError:
    import json


def GetArticleJsonDataApi(article_url: str) -> object:
    request_url = article_url.replace("https://www.jianshu.com/", "https://www.jianshu.com/asimov/")
    source = requests.get(request_url, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    return json_obj

def GetArticleHtmlJsonDataApi(article_url: str) -> object:
    source = requests.get(article_url, headers=PC_header).content
    html_obj = etree.HTML(source)
    json_obj = json.loads(html_obj.xpath("//script[@id='__NEXT_DATA__']/text()")[0])
    return json_obj

def GetArticleCommentsJsonDataApi(article_id: int, page: int, count: int, 
                                  author_only: bool, order_by: str) -> object:
    params = {
        "page": page, 
        "count": count, 
        "author_only": author_only, 
        "order_by": order_by
    }
    request_url = "https://www.jianshu.com/shakespeare/notes/" + str(article_id) + "/comments"
    source = requests.get(request_url, params=params, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    return json_obj

def GetBeikeIslandTradeRankListJsonDataApi(ranktype: int, pageIndex: int) -> object:
    params = {
        "ranktype": ranktype, 
        "pageIndex": pageIndex
    }
    source = requests.post("https://www.beikeisland.com/api/Trade/getTradeRankList", 
                            headers=BeikeIsland_request_header, json=params).content
    json_obj = json.loads(source)
    return json_obj

def GetBeikeIslandTradeListJsonDataApi(pageIndex: int, retype: int):
    params = {
        "pageIndex": pageIndex, 
        "retype": retype
    }
    source = requests.post("https://www.beikeisland.com/api/Trade/getTradeList", 
                            headers=BeikeIsland_request_header, json=params).content
    json_obj = json.loads(source)
    return json_obj

def GetCollectionJsonDataApi(collection_url: str) -> object:
    request_url = collection_url.replace("https://www.jianshu.com/c/", "https://www.jianshu.com/asimov/collections/slug/")
    source = requests.get(request_url, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    return json_obj

def GetCollectionEditorsJsonDataApi(collection_id: int, page: int) -> object:
    request_url = "https://www.jianshu.com/collections/" + str(collection_id) + "/editors"
    params = {
        "page": page
    }
    source = requests.get(request_url, params=params, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    return json_obj

def GetCollectionRecommendedWritersJsonDataApi(collection_id: int, page: int, count: int) -> object:
    params = {
        "collection_id": collection_id, 
        "page": page, 
        "count": count
    }
    source = requests.get("https://www.jianshu.com/collections/recommended_users", 
                            params=params, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    return json_obj

def GetCollectionSubscribersJsonDataApi(collection_id: int, max_sort_id: int) -> object:
    request_url = "https://www.jianshu.com/collection/" + str(collection_id) + "/subscribers"
    params = {
        "max_sort_id": max_sort_id
    }
    source = requests.get(request_url, params=params, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    return json_obj

def GetCollectionArticlesJsonDataApi(collection_slug: str, page: int, count: int, order_by: str) -> object:
    request_url = "https://www.jianshu.com/asimov/collections/slug/" + collection_slug + "/public_notes"
    params = {
        "page": page, 
        "count": count, 
        "order_by": order_by
    }
    source = requests.get(request_url, params=params, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    return json_obj

def GetIslandJsonDataApi(island_url: str) -> object:
    request_url = island_url.replace("https://www.jianshu.com/g/", "https://www.jianshu.com/asimov/groups/")
    source = requests.get(request_url, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    return json_obj

def GetIslandPostsJsonDataApi(group_slug: str, max_id: int, 
                           count: int, topic_id: int, order_by: str):
    params = {
        "group_slug": group_slug, 
        "order_by": order_by, 
        "max_id": max_id, 
        "count": count, 
        "topic_id": topic_id
    }
    source = requests.get("https://www.jianshu.com/asimov/posts", 
                            params=params, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    return json_obj

def GetNotebookJsonDataApi(notebook_url: str) -> object:
    request_url = notebook_url.replace("https://www.jianshu.com/", "https://www.jianshu.com/asimov/")
    source = requests.get(request_url, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    return json_obj

def GetNotebookArticlesJsonDataApi(notebook_url: str, page: int, 
                                count: int, order_by: str) -> object:
    request_url = notebook_url.replace("https://www.jianshu.com/nb/", 
            "https://www.jianshu.com/asimov/notebooks/") + "/public_notes/"
    params = {
        "page": page, 
        "count": count, 
        "order_by": order_by
    }
    source = requests.get(request_url, params=params, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    return json_obj

def GetAssetsRankJsonDataApi(max_id: int, since_id: int) -> object:
    params = {
        "max_id": max_id, 
        "since_id": since_id
    }
    source = requests.get("https://www.jianshu.com/asimov/fp_rankings", params=params, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    return json_obj

def GetDailyArticleRankListJsonDataApi() -> object:
    source = requests.get("https://www.jianshu.com/asimov/daily_activity_participants/rank", headers=jianshu_request_header).content
    json_obj = json.loads(source)
    return json_obj

def GetArticlesFPRankListJsonDataApi(date: str, type_: str) -> object:  # 避免覆盖内置函数
    params = {
        "date": date, 
        "type": type_
    }
    source = requests.get("https://www.jianshu.com/asimov/fp_rankings/voter_notes", params=params, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    return json_obj

def GetUserJsonDataApi(user_url: str) -> object:
    request_url = user_url.replace("https://www.jianshu.com/u/", "https://www.jianshu.com/asimov/users/slug/")
    source = requests.get(request_url, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    return json_obj

def GetUserPCHtmlDataApi(user_url: str) -> object:
    source = requests.get(user_url, headers=PC_header).content
    html_obj = etree.HTML(source)
    return html_obj

def GetUserCollectionsAndNotebooksJsonDataApi(user_url: str, user_slug: str) -> object:
    request_url = user_url.replace("/u/", "/users/") + "/collections_and_notebooks"
    params = {
        "slug": user_slug
    }
    source = requests.get(request_url, headers=jianshu_request_header, params=params).content
    json_obj = json.loads(source)
    return json_obj

def GetUserArticlesListJsonDataApi(user_url: str, page: int, 
                                count: int, order_by: str) -> object :
    request_url = user_url.replace("/u/", "/asimov/users/slug/") + "/public_notes"
    params = {
        "page": page, 
        "count": count, 
        "order_by": order_by
    }
    source = requests.get(request_url, headers=jianshu_request_header, params=params).content
    json_obj = json.loads(source)
    return json_obj

def GetUserFollowingListHtmlDataApi(user_url: str, page: int):
    request_url = user_url.replace("/u/", "/users/") + "/following"
    params = {
        "page": page
    }
    source = requests.get(request_url, headers=PC_header, params=params).content
    html_obj = etree.HTML(source)
    return html_obj

def GetUserFollowersListHtmlDataApi(user_url: str, page: int):
    request_url = user_url.replace("/u/", "/users/") + "/followers"
    params = {
        "page": page
    }
    source = requests.get(request_url, headers=PC_header, params=params).content
    html_obj = etree.HTML(source)
    return html_obj

def GetUserNextAnniversaryDayHtmlDataApi(user_slug: str):
    request_url = "https://www.jianshu.com/mobile/u/" + user_slug + "/anniversary"
    mobile_headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.134 Mobile Safari/537.36"
        }
    source = requests.get(request_url, headers=mobile_headers).content
    html_obj = etree.HTML(source)
    return html_obj

def GetIslandPostJsonDataApi(post_slug: str):
    request_url = "https://www.jianshu.com/asimov/posts/" + post_slug
    source = requests.get(request_url, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    return json_obj