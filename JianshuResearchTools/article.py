import json
import re
from datetime import datetime

import requests
from lxml import etree

from assert_funcs import AssertArticleStatusNormal, AssertArticleUrl
from headers import PC_header, jianshu_request_header, mobile_header


def GetArticleTitle(article_url: str) -> str:
    """获取文章标题

    Args:
        article_url (str): 文章 Url

    Returns:
        str: 文章标题
    """
    AssertArticleUrl(article_url)
    AssertArticleStatusNormal(article_url)
    request_url = article_url.replace("https://www.jianshu.com/", "https://www.jianshu.com/asimov/")
    source = requests.get(request_url, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    result = json_obj["public_title"]
    return result

def GetArticleAuthorName(article_url: str) -> str:
    AssertArticleUrl(article_url)
    AssertArticleStatusNormal(article_url)
    source = requests.get(article_url, headers=PC_header).content
    html_obj = etree.HTML(source)
    json_obj = json.loads(html_obj.xpath("//script[@id='__NEXT_DATA__']/text()")[0])
    result = json_obj["props"]["initialState"]["note"]["data"]["user"]["nickname"]
    return result

def GetArticleReadsCount(article_url: str) -> str:
    """获取文章阅读量

    Args:
        article_url (str): 文章 Url

    Returns:
        str: 文章阅读量
    """
    AssertArticleUrl(article_url)
    AssertArticleStatusNormal(article_url)
    source = requests.get(article_url, headers=PC_header).content
    html_obj = etree.HTML(source)
    json_obj = json.loads(html_obj.xpath("//script[@id='__NEXT_DATA__']/text()")[0])
    result = json_obj["props"]["initialState"]["note"]["data"]["views_count"]
    return result

def GetArticleWordsCount(article_url: str) -> str:
    """获取文章总字数

    Args:
        article_url (str): 文章 Url

    Returns:
        str: 文章总字数
    """
    AssertArticleUrl(article_url)
    AssertArticleStatusNormal(article_url)
    source = requests.get(article_url, headers=PC_header).content
    html_obj = etree.HTML(source)
    json_obj = json.loads(html_obj.xpath("//script[@id='__NEXT_DATA__']/text()")[0])
    result = json_obj["props"]["initialState"]["note"]["data"]["wordage"]
    return result

def GetArticleLikesCount(article_url: str) -> int:
    """获取文章点赞量

    Args:
        article_url (str): 文章 Url

    Returns:
        int: 文章点赞量
    """
    AssertArticleUrl(article_url)
    AssertArticleStatusNormal(article_url)
    request_url = article_url.replace("https://www.jianshu.com/", "https://www.jianshu.com/asimov/")
    source = requests.get(request_url, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    result = json_obj["likes_count"]
    return result

def GetArticleCommentsCount(article_url: str) -> int:
    """获取文章评论量

    Args:
        article_url (str): 文章 Url

    Returns:
        int: 文章评论量
    """
    AssertArticleUrl(article_url)
    AssertArticleStatusNormal(article_url)
    request_url = article_url.replace("https://www.jianshu.com/", "https://www.jianshu.com/asimov/")
    source = requests.get(request_url, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    result = json_obj["public_comment_count"]
    return result

def GetArticleMostValuableCommentsCount(article_url: str) -> int:
    """获取文章精选评论量

    Args:
        article_url (str): 文章 Url

    Returns:
        int: 文章精选评论量
    """
    AssertArticleUrl(article_url)
    AssertArticleStatusNormal(article_url)
    request_url = article_url.replace("https://www.jianshu.com/", "https://www.jianshu.com/asimov/")
    source = requests.get(request_url, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    result = json_obj["featured_comments_count"]
    return result

def GetArticleTotalFPCount(article_url: str) -> int:
    """获取文章总获钻量

    Args:
        article_url (str): 文章 Url

    Returns:
        int: 文章总获钻量
    """
    AssertArticleUrl(article_url)
    AssertArticleStatusNormal(article_url)
    request_url = article_url.replace("https://www.jianshu.com/", "https://www.jianshu.com/asimov/")
    source = requests.get(request_url, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    result = json_obj["total_fp_amount"] / 1000
    return result

def GetArticleDescription(article_url: str) -> str:
    """获取文章摘要

    Args:
        article_url (str): 文章 Url

    Returns:
        str: 文章摘要
    """
    AssertArticleUrl(article_url)
    AssertArticleStatusNormal(article_url)
    request_url = article_url.replace("https://www.jianshu.com/", "https://www.jianshu.com/asimov/")
    source = requests.get(request_url, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    result = json_obj["description"]
    return result

def GetArticlePublishTime(article_url: str) -> datetime:
    """获取文章发布时间

    Args:
        article_url (str): 文章 Url

    Returns:
        datetime: 文章发布时间
    """
    AssertArticleUrl(article_url)
    AssertArticleStatusNormal(article_url)
    request_url = article_url.replace("https://www.jianshu.com/", "https://www.jianshu.com/asimov/")
    source = requests.get(request_url, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    result = datetime.fromisoformat(json_obj["first_shared_at"])
    return result

def GetArticleUpdateTime(article_url: str) -> datetime:
    """获取文章更新时间

    Args:
        article_url (str): 文章 Url

    Returns:
        datetime: 文章更新时间
    """
    AssertArticleUrl(article_url)
    AssertArticleStatusNormal(article_url)
    request_url = article_url.replace("https://www.jianshu.com/", "https://www.jianshu.com/asimov/")
    source = requests.get(request_url, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    result = datetime.fromtimestamp(json_obj["last_updated_at"])
    return result

def GetArticlePaidStatus(article_url: str) -> bool:
    """获取文章付费状态

    Args:
        article_url (str): 文章 Url

    Returns:
        bool: 文章付费状态，True 为付费文章，False 为免费文章
    """
    AssertArticleUrl(article_url)
    AssertArticleStatusNormal(article_url)
    request_url = article_url.replace("https://www.jianshu.com/", "https://www.jianshu.com/asimov/")
    source = requests.get(request_url, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    paid_type = {
        "free": False, 
        "paid": True
    }
    result = paid_type[json_obj["paid_type"]]
    return result

def GetArticleReprintStatus(article_url: str) -> bool:  # TODO: 是不是要改个名？
    """获取文章转载声明状态

    Args:
        article_url (str): 文章 Url

    Returns:
        bool: 文章转载声明状态，True 为允许转载，False 为禁止转载
    """
    AssertArticleUrl(article_url)
    AssertArticleStatusNormal(article_url)
    request_url = article_url.replace("https://www.jianshu.com/", "https://www.jianshu.com/asimov/")
    source = requests.get(request_url, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    result = json_obj["reprintable"]
    return result

def GetArticleCommentStatus(article_url: str) -> bool:
    """获取文章评论状态

    Args:
        article_url (str): 文章 Url

    Returns:
        bool: 文章评论状态，True 为开启评论，False 为关闭评论
    """
    AssertArticleUrl(article_url)
    AssertArticleStatusNormal(article_url)
    request_url = article_url.replace("https://www.jianshu.com/", "https://www.jianshu.com/asimov/")
    source = requests.get(request_url, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    result = json_obj["commentable"]
    return result


def GetArticleHtml(article_url: str) -> str:
    """获取 Html 格式的文章内容

    # ! 该函数可以获取设置禁止转载的文章内容，请尊重作者版权，由此带来的风险由您自行承担
    # ! 该函数不能获取需要付费的文章内容
    # ! 文章中的图片描述将会丢失

    Args:
        article_url (str): 文章 Url

    Returns:
        str: Html 格式的文章内容
    """
    AssertArticleUrl(article_url)
    AssertArticleStatusNormal(article_url)
    request_url = article_url.replace("https://www.jianshu.com/", "https://www.jianshu.com/asimov/")
    source = requests.get(request_url, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    html_text = json_obj["free_content"]
    html_text = re.sub(r'\<div class="image-[\w]*" [ \w+-="]*>', "", html_text)  # 去除 image-view 和 image-container
    # TODO: 优化正则表达式，不去除 image-caption，即可保留图片描述
    html_text = re.sub(r'<div class=".+>', "", html_text)  # 去除 image-package、image-container-fill 和 image-caption
    old_img_blocks = re.findall(r'\<img[ \w+-="]*>', html_text)  # 匹配旧的 img 标签
    img_names = re.findall(r"\w+-\w+.[jpg | png]{3}",html_text)  # 获取图片名称
    new_img_blocks = ["".join(['<img src="https://upload-images.jianshu.io/upload_images/', \
                    img_name, '">']) for img_name in img_names]  # 拼接新的 img 标签
    for index in range(len(old_img_blocks)):
        if index == 0:
            replaced = html_text.replace(old_img_blocks[index], new_img_blocks[index])
        else:
            replaced = replaced.replace(old_img_blocks[index], new_img_blocks[index])  # 替换 img 标签
    return replaced

def GetArticleText(article_url: str) -> str:
    """获取纯文本格式的文章内容

    # ! 该函数可以获取设置禁止转载的文章内容，请尊重作者版权，由此带来的风险由您自行承担
    # ! 该函数不能获取需要付费的文章内容
    # ! 文章中的换行将会丢失

    Args:
        article_url (str): 文章 Url

    Returns:
        str: 纯文本格式的文章内容
    """
    AssertArticleUrl(article_url)
    AssertArticleStatusNormal(article_url)
    request_url = article_url.replace("https://www.jianshu.com/", "https://www.jianshu.com/asimov/")
    source = requests.get(request_url, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    html_text = json_obj["free_content"]
    html_obj = etree.HTML(html_text)
    # TODO: 优化筛选逻辑，保留单个空行
    result = "".join([item for item in html_obj.itertext() if item != "\n"])
    return result
