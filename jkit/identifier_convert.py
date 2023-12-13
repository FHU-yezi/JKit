from jkit.identifier_assert import (
    assert_article_slug,
    assert_article_url,
    assert_collection_slug,
    assert_collection_url,
    assert_island_slug,
    assert_island_url,
    assert_notebook_slug,
    assert_notebook_url,
    assert_user_slug,
    assert_user_url,
)


def user_url_to_slug(string: str, /) -> str:
    if not assert_user_url(string):
        raise ValueError(f"{string} 不是有效的 user_url")

    return string.replace("https://www.jianshu.com/u/", "").replace("/", "")


def user_slug_to_url(string: str, /) -> str:
    if not assert_user_slug(string):
        raise ValueError(f"{string} 不是有效的 user_slug")

    return f"https://www.jianshu.com/u/{string}"

def article_url_to_slug(string: str, /) -> str:
    if not assert_article_url(string):
        raise ValueError(f"{string} 不是有效的 article_url")

    return string.replace("https://www.jianshu.com/p/", "").replace("/", "")


def article_slug_to_url(string: str, /) -> str:
    if not assert_article_slug(string):
        raise ValueError(f"{string} 不是有效的 article_slug")

    return f"https://www.jianshu.com/p/{string}"

def notebook_url_to_slug(string: str, /) -> str:
    if not assert_notebook_url(string):
        raise ValueError(f"{string} 不是有效的 notebook_url")

    return string.replace("https://www.jianshu.com/nb/", "").replace("/", "")


def notebook_slug_to_url(string: str, /) -> str:
    if not assert_notebook_slug(string):
        raise ValueError(f"{string} 不是有效的 notebook_slug")

    return f"https://www.jianshu.com/nb/{string}"

def collection_url_to_slug(string: str, /) -> str:
    if not assert_collection_url(string):
        raise ValueError(f"{string} 不是有效的 collection_url")

    return string.replace("https://www.jianshu.com/c/", "").replace("/", "")


def collection_slug_to_url(string: str, /) -> str:
    if not assert_collection_slug(string):
        raise ValueError(f"{string} 不是有效的 collection_slug")

    return f"https://www.jianshu.com/c/{string}"

def island_url_to_slug(string: str, /) -> str:
    if not assert_island_url(string):
        raise ValueError(f"{string} 不是有效的 island_url")

    return string.replace("https://www.jianshu.com/g/", "").replace("/", "")


def island_slug_to_url(string: str, /) -> str:
    if not assert_island_slug(string):
        raise ValueError(f"{string} 不是有效的 island_slug")

    return f"https://www.jianshu.com/g/{string}"
