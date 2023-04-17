from .assert_funcs import (
    AssertArticleStatusNormal,
    AssertArticleUrl,
    AssertCollectionUrl,
    AssertIslandPostUrl,
    AssertIslandUrl,
    AssertNotebookUrl,
    AssertType,
    AssertUserUrl,
)
from .basic_apis import (
    GetArticleJsonDataApi,
    GetCollectionJsonDataApi,
    GetUserJsonDataApi,
)

__all__ = [
    "UserUrlToUserId",
    "UserSlugToUserId",
    "UserUrlToUserSlug",
    "ArticleUrlToArticleSlug",
    "ArticleSlugToArticleUrl",
    "ArticleSlugToArticleId",
    "ArticleUrlToArticleId",
    "NotebookUrlToNotebookId",
    "NotebookUrlToNotebookSlug",
    "CollectionSlugToCollectionUrl",
    "CollectionUrlToCollectionId",
    "IslandUrlToIslandSlug",
    "IslandSlugToIslandUrl",
    "UserUrlToUserUrlScheme",
    "ArticleUrlToArticleUrlScheme",
    "NotebookUrlToNotebookUrlScheme",
    "CollectionUrlToCollectionUrlScheme",
    "IslandPostUrlToIslandPostSlug",
    "IslandPostSlugToIslandPostUrl",
]


def UserUrlToUserId(user_url: str) -> int:
    """用户个人主页 URL 转用户 ID

    Args:
        user_url (str): 用户个人主页 URL

    Returns:
        int: 用户 ID
    """
    AssertType(user_url, str)
    AssertUserUrl(user_url)
    json_obj = GetUserJsonDataApi(user_url)
    return json_obj["id"]


def UserSlugToUserId(user_slug: str) -> int:
    """用户 Slug 转用户 ID

    Args:
        user_slug (str): 用户 Slug

    Returns:
        int: 用户 ID
    """
    AssertType(user_slug, str)
    user_url = UserSlugToUserUrl(user_slug)
    AssertUserUrl(user_url)
    return UserUrlToUserId(user_url)


def UserUrlToUserSlug(user_url: str) -> str:
    """用户个人主页 URL 转用户 Slug

    Args:
        user_url (str): 用户个人主页 URL

    Returns:
        str: 用户 Slug
    """
    AssertType(user_url, str)
    AssertUserUrl(user_url)
    return user_url.replace("https://www.jianshu.com/u/", "").replace("/", "")


def UserSlugToUserUrl(user_slug: str) -> str:
    """用户 Slug 转用户个人主页 URL

    Args:
        user_slug (str): 用户 Slug

    Returns:
        str: 用户个人主页 URL
    """
    AssertType(user_slug, str)
    result = f"https://www.jianshu.com/u/{user_slug}"
    AssertUserUrl(result)
    return result


def ArticleUrlToArticleSlug(article_url: str) -> str:
    """文章 URL 转文章 Slug

    Args:
        article_url (str): 文章 URL

    Returns:
        str: 文章 Slug
    """
    AssertType(article_url, str)
    AssertArticleUrl(article_url)
    return article_url.replace("https://www.jianshu.com/p/", "")


def ArticleSlugToArticleUrl(article_slug: str) -> str:
    """文章 Slug 转文章 URL

    Args:
        article_slug (str): 文章 Slug

    Returns:
        str: 文章 URL
    """
    AssertType(article_slug, str)
    result = f"https://www.jianshu.com/p/{article_slug}"
    AssertArticleUrl(result)
    return result


def ArticleSlugToArticleId(article_slug: str) -> int:
    """文章 Slug 转文章 ID

    Args:
        article_slug (str): 文章 Slug

    Returns:
        int: 文章 ID
    """
    AssertType(article_slug, str)
    json_obj = GetArticleJsonDataApi(ArticleSlugToArticleUrl(article_slug))
    return json_obj["id"]


def ArticleUrlToArticleId(article_url: str) -> int:
    """文章 URL 转文章 ID

    Args:
        article_url (str): 文章 URL

    Returns:
        int: 文章 ID
    """
    AssertType(article_url, str)
    AssertArticleUrl(article_url)
    AssertArticleStatusNormal(article_url)
    json_obj = GetArticleJsonDataApi(article_url)
    return json_obj["id"]


def NotebookUrlToNotebookId(notebook_url: str) -> int:
    """文集 URL 转文集 ID

    Args:
        notebook_url (str): 文集 URL

    Returns:
        int: 文集 ID
    """
    AssertType(notebook_url, str)
    AssertNotebookUrl(notebook_url)
    json_obj = GetArticleJsonDataApi(notebook_url)
    return json_obj["id"]


def NotebookUrlToNotebookSlug(notebook_url: str) -> str:
    """文集 URL 转文集 Slug

    Args:
        notebook_url (str): 文集 URL

    Returns:
        str: 文集 Slug
    """
    AssertType(notebook_url, str)
    AssertNotebookUrl(notebook_url)
    return notebook_url.replace("https://www.jianshu.com/nb/", "")


def NotebookSlugToNotebookUrl(notebook_slug: str) -> str:
    """文集 Slug 转文集 URL

    Args:
        notebook_slug (str): 文集 Slug

    Returns:
        str: 文集 URL
    """
    AssertType(notebook_slug, str)
    result = f"https://www.jianshu.com/nb/{notebook_slug}"
    AssertNotebookUrl(result)
    return result


def CollectionUrlToCollectionSlug(collection_url: str) -> str:
    """专题 URL 转专题 Slug

    Args:
        collection_url (str): 专题 URL

    Returns:
        str: 专题 Slug
    """
    AssertType(collection_url, str)
    AssertCollectionUrl(collection_url)
    return collection_url.replace("https://www.jianshu.com/c/", "")


def CollectionSlugToCollectionUrl(collection_slug: str) -> str:
    """专题 Slug 转专题 URL

    Args:
        collection_slug (str): 专题 Slug

    Returns:
        str: 专题 URL
    """
    AssertType(collection_slug, str)
    result = f"https://www.jianshu.com/c/{collection_slug}"
    AssertCollectionUrl(result)
    return result


def CollectionUrlToCollectionId(collection_url: str) -> int:
    """专题 URL 转专题 ID

    Args:
        collection_url (str): 专题 URL

    Returns:
        int: 专题 ID
    """
    AssertType(collection_url, str)
    AssertCollectionUrl(collection_url)
    return GetCollectionJsonDataApi(collection_url)["id"]


def IslandUrlToIslandSlug(island_url: str) -> str:
    """小岛 URL 转小岛 Slug

    Args:
        island_url (str): 小岛 URL

    Returns:
        str: 小岛 Slug
    """
    AssertType(island_url, str)
    AssertIslandUrl(island_url)
    return island_url.replace("https://www.jianshu.com/g/", "")


def IslandSlugToIslandUrl(island_slug: str) -> str:
    """小岛 Slug 转小岛 URL

    Args:
        island_slug (str): 小岛 Slug

    Returns:
        str: 小岛 URL
    """
    AssertType(island_slug, str)
    result = f"https://www.jianshu.com/g/{island_slug}"
    AssertIslandUrl(result)
    return result


def UserUrlToUserUrlScheme(user_url: str) -> str:
    """用户个人主页 URL 转用户个人主页 URL Scheme

    Args:
        user_url (str): 用户个人主页 URL
    Returns:
        str: 用户个人主页 URL Scheme
    """
    AssertType(user_url, str)
    AssertUserUrl(user_url)
    return user_url.replace("https://www.jianshu.com/u/", "jianshu://u/")


def ArticleUrlToArticleUrlScheme(article_url: str) -> str:
    """文章 URL 转文章 URL Scheme

    Args:
        article_url (str): 文章 URL
    Returns:
        str: 文章 URL Scheme
    """
    AssertType(article_url, str)
    AssertArticleUrl(article_url)
    return article_url.replace("https://www.jianshu.com/p/", "jianshu://notes/")


def NotebookUrlToNotebookUrlScheme(notebook_url: str) -> str:
    """文集 URL 转文集 URL Scheme

    Args:
        notebook_url (str): 文集 URL
    Returns:
        str: 文集 URL Scheme
    """
    AssertType(notebook_url, str)
    AssertNotebookUrl(notebook_url)
    return notebook_url.replace("https://www.jianshu.com/nb/", "jianshu://nb/")


def CollectionUrlToCollectionUrlScheme(collection_url: str) -> str:
    """文集 URL 转文集 URL Scheme

    Args:
        collection_url (str): 专题 URL
    Returns:
        str: 文集 URL Scheme
    """
    AssertType(collection_url, str)
    AssertCollectionUrl(collection_url)
    return collection_url.replace("https://www.jianshu.com/c/", "jianshu://c/")


def IslandPostUrlToIslandPostSlug(post_url: str) -> str:
    """小岛文章 URL 转小岛帖子 Slug

    Args:
        post_url (str): 小岛帖子 URL

    Returns:
        str: 小岛帖子 Slug
    """
    AssertType(post_url, str)
    AssertIslandPostUrl(post_url)
    return post_url.replace("https://www.jianshu.com/gp/", "")


def IslandPostSlugToIslandPostUrl(post_slug: str) -> str:
    """小岛帖子 Slug 转小岛帖子 URL

    Args:
        post_slug (str): 小岛帖子 Slug

    Returns:
        str: 小岛帖子 URL
    """
    AssertType(post_slug, str)
    result = f"https://www.jianshu.com/gp/{post_slug}"
    AssertIslandPostUrl(result)
    return result
