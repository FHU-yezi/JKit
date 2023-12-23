from re import compile as regex_compile

USER_NAME_REGEX = regex_compile(r"^[\w]*$")

JIANSHU_URL_REGEX = regex_compile(r"^https://www\.jianshu\.com/[a-z0-9/]*/?$")
USER_UPLOADED_URL_REGEX = regex_compile(r"^https:\/\/.*\.jianshu\.io\/[\w%-\/]*\/?$")
USER_URL_REGEX = regex_compile(r"^https://www\.jianshu\.com/u/[a-z0-9]{6,12}/?$")
ARTICLE_URL_REGEX = regex_compile(r"^https://www\.jianshu\.com/p/[a-z0-9]{12}/?$")
NOTEBOOK_URL_REGEX = regex_compile(r"^https://www\.jianshu\.com/nb/\d{7,8}/?$")
COLLECTION_URL_REGEX = regex_compile(r"^https://www\.jianshu\.com/c/[a-z0-9]{6,12}/?$")
ISLAND_URL_REGEX = regex_compile(r"^https://www\.jianshu\.com/g/[a-z0-9]{16}/?$")

USER_SLUG_REGEX = regex_compile(r"^[a-z0-9]{6,12}/?$")
ARTICLE_SLUG_REGEX = regex_compile(r"^[a-z0-9]{12}/?$")
NOTEBOOK_SLUG_REGEX = regex_compile(r"^\d{7,8}/?$")
COLLECTION_SLUG_REGEX = regex_compile(r"^[a-z0-9]{6,12}/?$")
ISLAND_SLUG_REGEX = regex_compile(r"^[a-z0-9]{16}/?$")

MAX_ID = 10**9
