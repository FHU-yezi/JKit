from jkit.constants import (
    ARTICLE_SLUG_REGEX,
    ARTICLE_URL_REGEX,
    COLLECTION_SLUG_REGEX,
    COLLECTION_URL_REGEX,
    ISLAND_SLUG_REGEX,
    ISLAND_URL_REGEX,
    NOTEBOOK_SLUG_REGEX,
    NOTEBOOK_URL_REGEX,
    USER_SLUG_REGEX,
    USER_URL_REGEX,
)


def assert_user_url(string: str, /) -> bool:
    return bool(USER_URL_REGEX.fullmatch(string))


def assert_article_url(string: str, /) -> bool:
    return bool(ARTICLE_URL_REGEX.fullmatch(string))


def assert_notebook_url(string: str, /) -> bool:
    return bool(NOTEBOOK_URL_REGEX.fullmatch(string))


def assert_collection_url(string: str, /) -> bool:
    return bool(COLLECTION_URL_REGEX.fullmatch(string))


def assert_island_url(string: str, /) -> bool:
    return bool(ISLAND_URL_REGEX.fullmatch(string))


def assert_user_slug(string: str, /) -> bool:
    return bool(USER_SLUG_REGEX.fullmatch(string))


def assert_article_slug(string: str, /) -> bool:
    return bool(ARTICLE_SLUG_REGEX.fullmatch(string))


def assert_notebook_slug(string: str, /) -> bool:
    return bool(NOTEBOOK_SLUG_REGEX.fullmatch(string))


def assert_collection_slug(string: str, /) -> bool:
    return bool(COLLECTION_SLUG_REGEX.fullmatch(string))


def assert_island_slug(string: str, /) -> bool:
    return bool(ISLAND_SLUG_REGEX.fullmatch(string))
