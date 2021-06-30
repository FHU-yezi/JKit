import json

import requests

from .exceptions import InputError, ResourceError
from .headers import jianshu_request_header

def AssertString(object: any) -> None:
    if isinstance(object, str) == False:
        raise TypeError("传入的数据不是字符串")

def AssertInt(object: any) -> None:
    if isinstance(object, int) == False:
        raise TypeError("传入的数据不是整数")

def AssertFloat(object: any) -> None:
    if isinstance(object, float) == False:
        raise TypeError("传入的数据不是浮点数")


def AssertJianshuUrl(string: str) -> None:
    """判断是否是有效的简书 Url

    Args:
        string (str): 需要进行判断的字符串

    Raises:
        InputError: 传入的参数不是有效的简书 Url 时抛出此错误
    """
    keyword_to_find = ["https://", "www.jianshu.com"]
    for keyword in keyword_to_find:
        if string.find(keyword) == -1:
            raise InputError("参数" + string + "不是有效的简书 Url")


def AssertUserUrl(string: str) -> None:
    """判断是否是有效的简书用户主页 Url

    Args:
        string (str): 需要进行判断的字符串

    Raises:
        InputError: 传入的参数不是有效的简书用户主页 Url 时抛出此错误
    """
    keyword_to_find = ["https://", "www.jianshu.com", "/u/"]
    for keyword in keyword_to_find:
        if string.find(keyword) == -1:
            raise InputError("参数" + string + "不是有效的简书用户主页 Url")

def AssertArticleUrl(string: str) -> None:
    """判断是否是有效的简书文章 Url

    Args:
        string (str): 需要进行判断的字符串

    Raises:
        InputError: 传入的参数不是有效的简书文章 Url 时抛出此错误
    """
    keyword_to_find = ["https://", "www.jianshu.com", "/p/"]
    for keyword in keyword_to_find:
        if string.find(keyword) == -1:
            raise InputError("参数" + string + "不是有效的简书文章 Url")

def AssertArticleStatusNormal(article_url: str) -> None:
    """判断文章状态是否正常

    Args:
        article_url (str): 文章 Url

    Raises:
        ResourceError: 文章状态不正常时抛出此错误
    """
    AssertArticleUrl(article_url)
    request_url = article_url.replace("https://www.jianshu.com/", "https://www.jianshu.com/asimov/")
    source = requests.get(request_url, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    try:
        json_obj["show_ad"]
    except KeyError:
        raise ResourceError("文章状态异常")

def AssertNotebookUrl(string: str) -> None:
    """判断是否是有效的简书文集 Url

    Args:
        string (str): 需要进行判断的字符串

    Raises:
        InputError: 传入的参数不是有效的简书文集 Url 时抛出此错误
    """
    keyword_to_find = ["https://", "www.jianshu.com", "/nb/"]
    for keyword in keyword_to_find:
        if string.find(keyword) == -1:
            raise InputError("参数" + string + "不是有效的简书文集 Url")
        
def AssertCollectionUrl(string: str) -> None:
    """判断是否是有效的简书专题 Url

    Args:
        string (str): 需要进行判断的字符串

    Raises:
        InputError: 传入的参数不是有效的简书专题 Url 时抛出此错误
    """
    keyword_to_find = ["https://", "www.jianshu.com", "/c/"]
    for keyword in keyword_to_find:
        if string.find(keyword) == -1:
            raise InputError("参数" + string + "不是有效的简书专题 Url")


def AssertIslandUrl(string: str) -> None:
    """判断是否是有效的简书小岛 Url

    Args:
        string (str): 需要进行判断的字符串

    Raises:
        InputError: 传入的参数不是有效的简书小岛 Url 时抛出此错误
    """
    keyword_to_find = ["https://", "www.jianshu.com", "/g/"]
    for keyword in keyword_to_find:
        if string.find(keyword) == -1:
            raise InputError("参数" + string + "不是有效的简书小岛 Url")