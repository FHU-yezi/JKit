def user_url_to_slug(url: str) -> str:
    return url.replace("https://www.jianshu.com/u/", "")


def user_slug_to_url(slug: str) -> str:
    return f"https://www.jianshu.com/u/{slug}"
