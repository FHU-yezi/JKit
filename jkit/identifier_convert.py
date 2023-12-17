from jkit.identifier_check import (
    is_article_slug,
    is_article_url,
    is_collection_slug,
    is_collection_url,
    is_island_slug,
    is_island_url,
    is_notebook_slug,
    is_notebook_url,
    is_user_slug,
    is_user_url,
)


def user_url_to_slug(string: str, /) -> str:
    if not is_user_url(string):
        raise ValueError(f"{string} 不是有效的 user_url")

    return string.replace("https://www.jianshu.com/u/", "").replace("/", "")


def user_slug_to_url(string: str, /) -> str:
    if not is_user_slug(string):
        raise ValueError(f"{string} 不是有效的 user_slug")

    return f"https://www.jianshu.com/u/{string}"


async def user_url_to_id(string: str, /) -> int:
    from jkit.user import User

    return await User.from_url(string).id


async def user_slug_to_id(string: str, /) -> int:
    from jkit.user import User

    return await User.from_slug(string).id


def article_url_to_slug(string: str, /) -> str:
    if not is_article_url(string):
        raise ValueError(f"{string} 不是有效的 article_url")

    return string.replace("https://www.jianshu.com/p/", "").replace("/", "")


def article_slug_to_url(string: str, /) -> str:
    if not is_article_slug(string):
        raise ValueError(f"{string} 不是有效的 article_slug")

    return f"https://www.jianshu.com/p/{string}"


def notebook_url_to_slug(string: str, /) -> str:
    if not is_notebook_url(string):
        raise ValueError(f"{string} 不是有效的 notebook_url")

    return string.replace("https://www.jianshu.com/nb/", "").replace("/", "")


def notebook_slug_to_url(string: str, /) -> str:
    if not is_notebook_slug(string):
        raise ValueError(f"{string} 不是有效的 notebook_slug")

    return f"https://www.jianshu.com/nb/{string}"


def collection_url_to_slug(string: str, /) -> str:
    if not is_collection_url(string):
        raise ValueError(f"{string} 不是有效的 collection_url")

    return string.replace("https://www.jianshu.com/c/", "").replace("/", "")


def collection_slug_to_url(string: str, /) -> str:
    if not is_collection_slug(string):
        raise ValueError(f"{string} 不是有效的 collection_slug")

    return f"https://www.jianshu.com/c/{string}"


def island_url_to_slug(string: str, /) -> str:
    if not is_island_url(string):
        raise ValueError(f"{string} 不是有效的 island_url")

    return string.replace("https://www.jianshu.com/g/", "").replace("/", "")


def island_slug_to_url(string: str, /) -> str:
    if not is_island_slug(string):
        raise ValueError(f"{string} 不是有效的 island_slug")

    return f"https://www.jianshu.com/g/{string}"
