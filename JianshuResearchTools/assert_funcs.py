try:
    import ujson as json
except ImportError:
    import json

from functools import lru_cache
from typing import Any

from .basic_apis import (GetArticleJsonDataApi, GetCollectionJsonDataApi,
                         GetIslandJsonDataApi, GetUserJsonDataApi)
from .exceptions import InputError, ResourceError


def AssertType(object: Any, type_obj: Any) -> None:
    """判断对象是否是指定类型

    Args:
        object (Any): 需要进行判断的对象
        type_obj (object): 需要判断的类型

    Raises:
        TypeError: 传入的对象不是指定类型时抛出此错误
    """
    if isinstance(object, type_obj) == False:
        raise TypeError(f"传入的对象不是 {type_obj.__name__} 类型")
    

def AssertString(object: Any) -> None:
    if isinstance(object, str) == False:
        raise TypeError("传入的数据不是字符串")
    raise DeprecationWarning("该函数已过时，将在下个版本中移除，请使用 AssertType 函数")

def AssertInt(object: Any) -> None:
    if isinstance(object, int) == False:
        raise TypeError("传入的数据不是整数")
    raise DeprecationWarning("该函数已过时，将在下个版本中移除，请使用 AssertType 函数")

def AssertFloat(object: Any) -> None:
    if isinstance(object, float) == False:
        raise TypeError("传入的数据不是浮点数")
    raise DeprecationWarning("该函数已过时，将在下个版本中移除，请使用 AssertType 函数")


def AssertJianshuUrl(string: str) -> None:
    """判断是否是有效的简书 Url

    Args:
        string (str): 需要进行判断的字符串

    Raises:
        InputError: 传入的参数不是有效的简书 Url 时抛出此错误
    """
    keyword_to_find = ["https://", "www.jianshu.com"]
    for keyword in keyword_to_find:
        if keyword not in string:
            raise InputError(f"参数 {string} 不是有效的简书 Url")


def AssertUserUrl(string: str) -> None:
    """判断是否是有效的简书用户主页 Url

    Args:
        string (str): 需要进行判断的字符串

    Raises:
        InputError: 传入的参数不是有效的简书用户主页 Url 时抛出此错误
    """
    keyword_to_find = ["https://", "www.jianshu.com", "/u/"]
    for keyword in keyword_to_find:
        if keyword not in string:
            raise InputError(f"参数 {string} 不是有效的简书用户主页 Url")

@lru_cache(maxsize=64)
def AssertUserStatusNormal(user_url: str) -> None:
    user_json_data = GetUserJsonDataApi(user_url)
    try:
        user_json_data["nickname"]
    except KeyError:
        raise ResourceError("用户账号状态异常")

def AssertArticleUrl(string: str) -> None:
    """判断是否是有效的简书文章 Url

    Args:
        string (str): 需要进行判断的字符串

    Raises:
        InputError: 传入的参数不是有效的简书文章 Url 时抛出此错误
    """
    keyword_to_find = ["https://", "www.jianshu.com", "/p/"]
    for keyword in keyword_to_find:
        if keyword not in string:
            raise InputError(f"参数 {string} 不是有效的简书文章 Url")

@lru_cache(maxsize=64)
def AssertArticleStatusNormal(article_url: str) -> None:
    """判断文章状态是否正常

    Args:
        article_url (str): 文章 Url

    Raises:
        ResourceError: 文章状态不正常时抛出此错误
    """
    AssertArticleUrl(article_url)
    json_obj = GetArticleJsonDataApi(article_url)
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
        if keyword not in string:
            raise InputError(f"参数 {string} 不是有效的简书文集 Url")
        
def AssertCollectionUrl(string: str) -> None:
    """判断是否是有效的简书专题 Url

    Args:
        string (str): 需要进行判断的字符串

    Raises:
        InputError: 传入的参数不是有效的简书专题 Url 时抛出此错误
    """
    keyword_to_find = ["https://", "www.jianshu.com", "/c/"]
    for keyword in keyword_to_find:
        if keyword not in string:
            raise InputError(f"参数 {string} 不是有效的简书专题 Url")

@lru_cache(maxsize=64)
def AssertCollectionStatusNormal(collection_url: str) -> None:
    collection_json_data = GetCollectionJsonDataApi(collection_url)
    try:
        collection_json_data["title"]
    except KeyError:
        raise ResourceError("专题状态异常")


def AssertIslandUrl(string: str) -> None:
    """判断是否是有效的简书小岛 Url

    Args:
        string (str): 需要进行判断的字符串

    Raises:
        InputError: 传入的参数不是有效的简书小岛 Url 时抛出此错误
    """
    keyword_to_find = ["https://", "www.jianshu.com", "/g/"]
    for keyword in keyword_to_find:
        if keyword not in string:
            raise InputError(f"参数 {string} 不是有效的简书小岛 Url")
        
@lru_cache(maxsize=64)
def AssertIslandStatusNormal(island_url: str) -> None:
    island_json_data = GetIslandJsonDataApi(island_url)
    try:
        island_json_data["name"]
    except KeyError:
        raise ResourceError("小岛状态异常")

def AssertIslandPostUrl(string: str) -> None:
    """判断是否是有效的简书小岛帖子 Url

    Args:
        string (str): 需要进行判断的字符串

    Raises:
        InputError: 传入的参数不是有效的简书小岛帖子 Url 时抛出此错误
    """
    keyword_to_find = ["https://", "www.jianshu.com", "/gp/"]
    for keyword in keyword_to_find:
        if keyword not in string:
            raise InputError(f"参数 {string} 不是有效的简书小岛帖子 Url")
