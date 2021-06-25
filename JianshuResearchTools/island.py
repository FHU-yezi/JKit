import requests
import json
from assert_funcs import AssertIslandUrl
from lxml import etree
from basic import PC_header, jianshu_request_header
import re
from convert import IslandUrlToIslandSlug
from datetime import datetime

def GetIslandName(island_url: str) -> str:
    AssertIslandUrl(island_url)
    source = requests.get(island_url, headers=PC_header).content.decode()  # TODO: 不知道为什么会出现编码问题
    html_obj = etree.HTML(source)
    result = html_obj.xpath("//div[@class='nickname']/text()")[0]
    result = result.strip()
    return result

def GetIslandIntroduction(island_url: str) -> str:
    AssertIslandUrl(island_url)
    source = requests.get(island_url, headers=PC_header).content.decode()  # TODO: 不知道为什么会出现编码问题
    html_obj = etree.HTML(source)
    result = html_obj.xpath("//div[@class='info']/text()")[0]
    result = result.strip()
    return result

def GetIslandMembersCount(island_url: str) -> int:
    AssertIslandUrl(island_url)
    source = requests.get(island_url, headers=PC_header).content.decode()  # TODO: 不知道为什么会出现编码问题
    html_obj = etree.HTML(source)
    result = html_obj.xpath("//div[@class='info']/text()")[1]
    result = re.findall(r"\d+", result)[0]
    return result

def GetIslandPosts(island_url: str, start_sort_id: int =None, count: int =10, 
                    topic_id: int =None, sorting_method: str ="time") -> list:
    AssertIslandUrl(island_url)
    params = {
        "group_slug": IslandUrlToIslandSlug(island_url), 
        "order_by": {
            "time": "latest", 
            "hot": "hot", 
            "most_valuable": "best"
        }[sorting_method], 
        "max_id": start_sort_id, 
        "count": count, 
        "topic_id": topic_id
    }
    source = requests.get("https://www.jianshu.com/asimov/posts", 
                            params=params, headers=jianshu_request_header).content
    json_obj = json.loads(source)

    result = []
    for item in json_obj:
        item_info = {
            "sorted_id": item["sorted_id"], 
            "pid": item["id"], 
            "pslug": item["slug"], 
            "title": item["title"], 
            "content": item["content"],   # TODO: 这里获取到的信息不完整
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
                "avatar": item["user"]["avatar"]
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
            item_info["user"]["badge"] = item["user"]["badge"]["text"]
        except KeyError:
            pass  # 没有徽章则跳过
        try:
            item_info["topic"] = {
                "tid": item["topic"]["id"], 
                "tslug": item["topic"]["slug"], 
                "topic_name": item["topic"]["name"]
                # 有个 group_role 不知道干什么用的，没解析
            }
        except KeyError:
            pass  # 没有话题则跳过
        result.append(item_info)
    return result