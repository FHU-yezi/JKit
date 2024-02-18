from jkit.identifier_check import (
    is_article_slug,
    is_article_url,
    is_collection_slug,
    is_collection_url,
    is_island_slug,
    is_island_url,
    is_notebook_id,
    is_notebook_url,
    is_user_slug,
    is_user_url,
)


def user_url_to_slug(x: str, /) -> str:
    if not is_user_url(x):
        raise ValueError(f"{x} 不是有效的用户链接")

    return x.replace("https://www.jianshu.com/u/", "").replace("/", "")


def user_slug_to_url(x: str, /) -> str:
    if not is_user_slug(x):
        raise ValueError(f"{x} 不是有效的用户 Slug")

    return f"https://www.jianshu.com/u/{x}"


async def user_url_to_id(x: str, /) -> int:
    from jkit.user import User

    return await User.from_url(x).id


async def user_slug_to_id(x: str, /) -> int:
    from jkit.user import User

    return await User.from_slug(x).id


def article_url_to_slug(x: str, /) -> str:
    if not is_article_url(x):
        raise ValueError(f"{x} 不是有效的文章链接")

    return x.replace("https://www.jianshu.com/p/", "").replace("/", "")


def article_slug_to_url(x: str, /) -> str:
    if not is_article_slug(x):
        raise ValueError(f"{x} 不是有效的文章 Slug")

    return f"https://www.jianshu.com/p/{x}"


def notebook_url_to_id(x: str, /) -> int:
    if not is_notebook_url(x):
        raise ValueError(f"{x} 不是有效的文集链接")

    return int(x.replace("https://www.jianshu.com/nb/", "").replace("/", ""))


def notebook_id_to_url(x: int, /) -> str:
    if not is_notebook_id(x):
        raise ValueError(f"{x} 不是有效的文集 ID")

    return f"https://www.jianshu.com/nb/{x}"


def collection_url_to_slug(x: str, /) -> str:
    if not is_collection_url(x):
        raise ValueError(f"{x} 不是有效的专题链接")

    return x.replace("https://www.jianshu.com/c/", "").replace("/", "")


def collection_slug_to_url(x: str, /) -> str:
    if not is_collection_slug(x):
        raise ValueError(f"{x} 不是有效的专题 Slug")

    return f"https://www.jianshu.com/c/{x}"


def island_url_to_slug(x: str, /) -> str:
    if not is_island_url(x):
        raise ValueError(f"{x} 不是有效的小岛链接")

    return x.replace("https://www.jianshu.com/g/", "").replace("/", "")


def island_slug_to_url(x: str, /) -> str:
    if not is_island_slug(x):
        raise ValueError(f"{x} 不是有效的小岛 Slug")

    return f"https://www.jianshu.com/g/{x}"
