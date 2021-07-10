try:
    import simplejson as json
except ImportError:
    import json

from .basic_apis import GetUserJsonDataApi, GetArticleJsonDataApi

from .assert_funcs import (AssertArticleStatusNormal, AssertArticleUrl,
                           AssertCollectionUrl, AssertIslandUrl,
                           AssertNotebookUrl, AssertString, AssertUserUrl)
from .headers import jianshu_request_header


def UserUrlToUserId(user_url: str) -> int:
    """该函数接收用户个人主页 Url，并将其转换成用户 Id

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        int: 用户 Id
    """
    AssertString(user_url)
    AssertUserUrl(user_url)
    json_obj = GetUserJsonDataApi(user_url)
    result = json_obj["id"]
    return result

def UserSlugToUserId(user_slug: str) -> int:
    """该函数接收用户 Slug，并将其转换成用户 Id

    Args:
        user_url (str): 用户 Slug

    Returns:
        int: 用户 Id
    """
    AssertString(user_slug)
    user_url = UserSlugToUserUrl(user_slug)
    AssertUserUrl(user_url)
    result = UserUrlToUserId(user_url)
    return result
    

def UserUrlToUserSlug(user_url: str) -> str:
    """该函数接收用户个人主页 Url，并将其转换成用户 Slug

    Args:
        user_url (str): 用户个人主页 Url

    Returns:
        str: 用户 Slug
    """
    AssertString(user_url)
    AssertUserUrl(user_url)
    return user_url.replace("https://www.jianshu.com/u/", "").replace("/", "")

def UserSlugToUserUrl(user_slug: str) -> str:
    """该函数接收用户 Slug，并将其转换成用户个人主页 Url

    Args:
        user_slug (str): 用户 Slug

    Returns:
        str: 用户个人主页 Url
    """
    AssertString(user_slug)
    result = "https://www.jianshu.com/u/" + user_slug
    AssertUserUrl(result)
    return result


def ArticleUrlToArticleSlug(article_url: str) -> str:
    """该函数接收文章 Url，并将其转换成文章 Slug

    Args:
        article_url (str): 文章 Url

    Returns:
        str: 文章 Slug
    """
    AssertString(article_url)
    AssertArticleUrl(article_url)
    return article_url.replace("https://www.jianshu.com/p/", "")

def ArticleSlugToArticleUrl(article_slug: str) -> str:
    """该函数接收文章 Slug，并将其转换成文章 Url

    Args:
        article_slug (str): 文章 Slug

    Returns:
        str: 文章 Url
    """
    AssertString(article_slug)
    result = "https://www.jianshu.com/p/" + article_slug
    AssertArticleUrl(result)
    return result

def ArticleSlugToArticleId(article_url: str) -> int:
    """该函数接收文章 Slug，并将其转换成文章 Id

    Args:
        article_slug (str): 文章 Slug

    Returns:
        int: 文章 Id
    """
    AssertString(article_url)
    AssertArticleUrl(article_url)
    AssertArticleStatusNormal(article_url)
    json_obj = GetArticleJsonDataApi(article_url)
    result = json_obj["id"]
    return result


def NotebookUrlToNotebookId(notebook_url: str) -> int:
    """该函数接收文集 Url，并将其转换成文集 Id

    Args:
        notebook_url (str): 文集 Url

    Returns:
        int: 文集 Id
    """
    AssertString(notebook_url)
    AssertNotebookUrl(notebook_url)
    json_obj = GetArticleJsonDataApi(notebook_url)
    result = json_obj["id"]
    return result

def NotebookUrlToNotebookSlug(notebook_url: str) -> str:
    """该函数接收文集 Url，并将其转换成文集 Slug

    Args:
        notebook_url (str): 文集 Url

    Returns:
        str: 文集 Slug
    """
    AssertString(notebook_url)
    AssertNotebookUrl(notebook_url)
    return notebook_url.replace("https://www.jianshu.com/nb/", "")

def NotebookSlugToNotebookUrl(notebook_slug: str) -> str:
    """该函数接收文集 Slug，并将其转换成文集 Url

    Args:
        notebook_slug (str): 文集 Slug

    Returns:
        str: 文集 Url
    """
    AssertString(notebook_slug)
    result = "https://www.jianshu.com/nb/" + notebook_slug
    AssertNotebookUrl(result)
    return result


def CollectionUrlToCollectionSlug(collection_url: str) -> str:
    """该函数接收专题 Url，并将其转换成专题 Slug

    Args:
        collection_url (str): 专题 Url

    Returns:
        str: 专题 Slug
    """
    AssertString(collection_url)
    AssertCollectionUrl(collection_url)
    return collection_url.replace("https://www.jianshu.com/c/", "")

def CollectionSlugToCollectionUrl(collection_slug: str) -> str:
    """该函数接收专题 Slug，并将其转换成专题 Url

    Args:
        collection_slug (str): 专题 Slug

    Returns:
        str: 专题 Url
    """
    AssertString(collection_slug)
    result = "https://www.jianshu.com/c/" + collection_slug
    AssertCollectionUrl(result)
    return result


def IslandUrlToIslandSlug(island_url: str) -> str:
    """该函数接收小岛 Url，并将其转换成小岛 Slug

    Args:
        island_url (str): 小岛 Url

    Returns:
        str: 小岛 Slug
    """
    AssertString(island_url)
    AssertIslandUrl(island_url)
    return island_url.replace("https://www.jianshu.com/g/", "")

def IslandSlugToIslandUrl(island_slug: str) -> str:
    """该函数接收小岛 Slug，并将其转换成小岛 Url

    Args:
        island_slug (str): 小岛 Slug

    Returns:
        str: 小岛 Url
    """
    AssertString(island_slug)
    result = "https://www.jianshu.com/g/" + island_slug
    AssertIslandUrl(result)
    return result

def UserUrlToUserUrlScheme(user_url: str) -> str:
    """该函数接收用户个人主页 Url，并返回跳转到简书 App 中对应用户的 Url Scheme

    Args:
        user_url (str): 用户个人主页 Url
    Returns:
        str: 跳转到简书 App 中对应用户的 Url Scheme
    """
    AssertString(user_url)
    AssertUserUrl(user_url)
    result = user_url.replace("https://www.jianshu.com/u/", "jianshu://u/")
    return result

def ArticleUrlToArticleUrlScheme(article_url: str) -> str:
    """该函数接收文章 Url，并返回跳转到简书 App 中对应文章的 Url Scheme

    Args:
        article_url (str): 文章 Url
    Returns:
        str: 跳转到简书 App 中对应文章的 Url Scheme
    """
    AssertString(article_url)
    AssertArticleUrl(article_url)
    result = article_url.replace("https://www.jianshu.com/p/", "jianshu://notes/")
    return result

def NotebookUrlToNotebookUrlScheme(notebook_url: str) -> str:
    """该函数接收文集 Url，并返回跳转到简书 App 中对应文集的 Url Scheme

    Args:
        notebook_url (str): 文集 Url
    Returns:
        str: 跳转到简书 App 中对应文集的 Url Scheme
    """
    AssertString(notebook_url)
    AssertNotebookUrl(notebook_url)
    result = notebook_url.replace("https://www.jianshu.com/nb/", "jianshu://nb/")
    return result

def CollectionUrlToCollectionUrlScheme(collection_url: str) -> str:
    """该函数接收专题 Url，并返回跳转到简书 App 中对应专题的 Url Scheme

    Args:
        collection_url (str): 专题 Url
    Returns:
        str: 跳转到简书 App 中对应专题的 Url Scheme
    """
    AssertString(collection_url)
    AssertCollectionUrl(collection_url)
    result = collection_url.replace("https://www.jianshu.com/c/", "jianshu://c/")
    return result
