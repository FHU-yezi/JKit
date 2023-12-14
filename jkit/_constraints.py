from datetime import datetime
from typing import Annotated

from msgspec import Meta

from jkit.constants import (
    ARTICLE_SLUG_REGEX,
    ARTICLE_URL_REGEX,
    COLLECTION_SLUG_REGEX,
    COLLECTION_URL_REGEX,
    ISLAND_SLUG_REGEX,
    ISLAND_URL_REGEX,
    JIANSHU_URL_REGEX,
    NOTEBOOK_SLUG_REGEX,
    NOTEBOOK_URL_REGEX,
    UPLOAD_JIANSHU_IO_URL_REGEX,
    USER_NAME_REGEX,
    USER_SLUG_REGEX,
    USER_URL_REGEX,
)

PositiveInt = Annotated[int, Meta(gt=0)]
NonNegativeInt = Annotated[int, Meta(ge=0)]
NonEmptyStr = Annotated[str, Meta(min_length=1)]
NormalizedDatetime = Annotated[datetime, Meta(tz=False)]

UserNameStr = Annotated[str, Meta(pattern=USER_NAME_REGEX.pattern)]

JianshuUrlStr = Annotated[str, Meta(pattern=JIANSHU_URL_REGEX.pattern)]
UploadJianshuIoUrlStr = Annotated[
    str, Meta(pattern=UPLOAD_JIANSHU_IO_URL_REGEX.pattern)
]
UserUrlStr = Annotated[str, Meta(pattern=USER_URL_REGEX.pattern)]
ArticleUrlStr = Annotated[str, Meta(pattern=ARTICLE_URL_REGEX.pattern)]
NotebookUrlStr = Annotated[str, Meta(pattern=NOTEBOOK_URL_REGEX.pattern)]
CollectionUrlStr = Annotated[str, Meta(pattern=COLLECTION_URL_REGEX.pattern)]
IslandUrlStr = Annotated[str, Meta(pattern=ISLAND_URL_REGEX.pattern)]

UserSlugStr = Annotated[str, Meta(pattern=USER_SLUG_REGEX.pattern)]
ArticleSlugStr = Annotated[str, Meta(pattern=ARTICLE_SLUG_REGEX.pattern)]
NotebookSlugStr = Annotated[str, Meta(pattern=NOTEBOOK_SLUG_REGEX.pattern)]
CollectionSlugStr = Annotated[str, Meta(pattern=COLLECTION_SLUG_REGEX.pattern)]
IslandSlugStr = Annotated[str, Meta(pattern=ISLAND_SLUG_REGEX.pattern)]
