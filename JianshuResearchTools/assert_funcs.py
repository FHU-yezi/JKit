from functools import lru_cache
from typing import Any
from re import compile as re_compile

from .basic_apis import (GetArticleJsonDataApi, GetCollectionJsonDataApi,
                         GetIslandJsonDataApi, GetNotebookJsonDataApi,
                         GetUserJsonDataApi)
from .exceptions import InputError, ResourceError

__all__ = [
    "JIANSHU_URL_REGEX", "JIANSHU_USER_URL_REGEX",
    "JIANSHU_ARTICLES_URL_REGEX", "JIANSHU_NOTEBOOK_URL_REGEX",
    "JIANSHU_COLLECTION_URL_REGEX", "JIANSHU_ISLAND_URL_REGEX",
    "JIANSHU_ISLAND_POST_URL_REGEX", "AssertType", "AssertJianshuUrl",
    "AssertUserUrl", "AssertUserStatusNormal", "AssertArticleUrl",
    "AssertArticleStatusNormal", "AssertCollectionUrl",
    "AssertCollectionStatusNormal", "AssertIslandUrl",
    "AssertIslandStatusNormal", "AssertIslandPostUrl"
]


JIANSHU_URL_REGEX = re_compile(r"^https://www\.jianshu\.com/\w{1,2}/\w{6,16}/?$")
JIANSHU_USER_URL_REGEX = re_compile(r"^https://www\.jianshu\.com/u/\w{6,12}/?$")
JIANSHU_ARTICLES_URL_REGEX = re_compile(r"^https://www\.jianshu\.com/p/\w{12}/?$")
JIANSHU_NOTEBOOK_URL_REGEX = re_compile(r"^https://www\.jianshu\.com/nb/\d{7,8}/?$")
JIANSHU_COLLECTION_URL_REGEX = re_compile(r"^https://www\.jianshu\.com/c/\w{6,12}/?$")
JIANSHU_ISLAND_URL_REGEX = re_compile(r"^https://www\.jianshu\.com/g/\w{16}/?$")
JIANSHU_ISLAND_POST_URL_REGEX = re_compile(r"^https://www\.jianshu\.com/gp/\w{16}/?$")


def AssertType(object: Any, type_obj: Any) -> None:
    """判断对象是否是指定类型

    Args:
        object (Any): 需要进行判断的对象
        type_obj (object): 目标类型

    Raises:
        TypeError: 对象类型错误时抛出此错误
    """
    if not isinstance(object, type_obj):
        raise TypeError(f"{object} 不是 {type_obj.__name__} 类型，而是 { type(object).__name__ } 类型")


def AssertJianshuUrl(string: str) -> None:
    """判断字符串是否是有效的简书 URL

    Args:
        string (str): 需要进行判断的字符串

    Raises:
        InputError: 字符串不是有效的简书 URL 时抛出此错误
    """
    if not JIANSHU_URL_REGEX.fullmatch(string):
        raise InputError(f"{string} 不是有效的简书 URL")


def AssertUserUrl(string: str) -> None:
    """判断字符串是否是有效的简书用户主页 URL

    Args:
        string (str): 需要进行判断的字符串

    Raises:
        InputError: 字符串不是有效的简书用户主页 URL 时抛出此错误
    """
    if not JIANSHU_USER_URL_REGEX.fullmatch(string):
        raise InputError(f"{string} 不是有效的简书用户主页 URL")


@lru_cache(maxsize=64)
def AssertUserStatusNormal(user_url: str) -> None:
    """判断用户账号状态是否正常

    Args:
        user_url (str): 用户主页 URL

    Raises:
        ResourceError: 用户账号状态异常时抛出此错误
    """
    user_json_data = GetUserJsonDataApi(user_url)
    try:
        user_json_data["nickname"]
    except KeyError:
        raise ResourceError(f"用户 {user_url} 账号状态异常")


def AssertArticleUrl(string: str) -> None:
    """判断字符串是否是有效的简书文章 URL

    Args:
        string (str): 需要进行判断的字符串

    Raises:
        InputError: 字符串不是有效的简书文章 URL 时抛出此错误
    """
    if not JIANSHU_ARTICLES_URL_REGEX.fullmatch(string):
        raise InputError(f"{string} 不是有效的简书文章 URL")


@lru_cache(maxsize=64)
def AssertArticleStatusNormal(article_url: str) -> None:
    """判断文章状态是否正常

    Args:
        article_url (str): 文章 URL

    Raises:
        ResourceError: 文章状态异常时抛出此错误
    """
    AssertArticleUrl(article_url)
    json_obj = GetArticleJsonDataApi(article_url)
    try:
        json_obj["show_ad"]
    except KeyError:
        raise ResourceError(f"文章 {article_url} 状态异常")


def AssertNotebookUrl(string: str) -> None:
    """判断字符串是否是有效的简书文集 URL

    Args:
        string (str): 需要进行判断的字符串

    Raises:
        InputError: 字符串不是有效的简书文集 URL 时抛出此错误
    """
    if not JIANSHU_NOTEBOOK_URL_REGEX.fullmatch(string):
        raise InputError(f"{string} 不是有效的简书文集 URL")


def AssertNotebookStatusNormal(notebook_url: str) -> None:
    """判断文集状态是否正常

    Args:
        notebook_url (str): 文集 URL

    Raises:
        ResourceError: 文集状态异常时抛出此错误
    """
    AssertNotebookUrl(notebook_url)
    json_obj = GetNotebookJsonDataApi(notebook_url)
    try:
        json_obj["name"]
    except KeyError:
        raise ResourceError(f"文集 {notebook_url} 状态异常")


def AssertCollectionUrl(string: str) -> None:
    """判断字符串是否是有效的简书专题 URL

    Args:
        string (str): 需要进行判断的字符串

    Raises:
        InputError: 字符串不是有效的简书专题 URL 时抛出此错误
    """
    if not JIANSHU_COLLECTION_URL_REGEX.fullmatch(string):
        raise InputError(f"{string} 不是有效的简书专题 URL")


@lru_cache(maxsize=64)
def AssertCollectionStatusNormal(collection_url: str) -> None:
    """判断专题状态是否正常

    Args:
        collection_url (str): 专题 URL

    Raises:
        ResourceError: 专题状态异常时抛出此错误
    """
    collection_json_data = GetCollectionJsonDataApi(collection_url)
    try:
        collection_json_data["title"]
    except KeyError:
        raise ResourceError(f"专题 {collection_url} 状态异常")


def AssertIslandUrl(string: str) -> None:
    """判断字符串是否是有效的简书小岛 URL

    Args:
        string (str): 需要进行判断的字符串

    Raises:
        InputError: 字符串不是有效的简书小岛 URL 时抛出此错误
    """
    if not JIANSHU_ISLAND_URL_REGEX.fullmatch(string):
        raise InputError(f"{string} 不是有效的简书小岛 URL")


@lru_cache(maxsize=64)
def AssertIslandStatusNormal(island_url: str) -> None:
    island_json_data = GetIslandJsonDataApi(island_url)
    try:
        island_json_data["name"]
    except KeyError:
        raise ResourceError(f"小岛 {island_url} 状态异常")


def AssertIslandPostUrl(string: str) -> None:
    """判断字符串是否是有效的简书小岛帖子 URL

    Args:
        string (str): 需要进行判断的字符串

    Raises:
        InputError: 字符串不是有效的简书小岛帖子 URL 时抛出此错误
    """
    if not JIANSHU_ISLAND_POST_URL_REGEX.fullmatch(string):
        raise InputError(f"{string} 不是有效的简书小岛帖子 URL")
