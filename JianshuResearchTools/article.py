from contextlib import suppress
from datetime import datetime
from re import findall, sub
from typing import Dict, Generator, List, Literal, Optional

from lxml import etree

from .assert_funcs import AssertArticleStatusNormal, AssertArticleUrl
from .basic_apis import (
    GetArticleCommentsJsonDataApi,
    GetArticleHtmlJsonDataApi,
    GetArticleJsonDataApi,
)

with suppress(ImportError):
    from tomd import convert as html2md

__all__ = [
    "GetArticleTitle",
    "GetArticleAuthorName",
    "GetArticleReadsCount",
    "GetArticleWordage",
    "GetArticleLikesCount",
    "GetArticleCommentsCount",
    "GetArticleMostValuableCommentsCount",
    "GetArticleTotalFPCount",
    "GetArticleDescription",
    "GetArticlePublishTime",
    "GetArticleUpdateTime",
    "GetArticlePaidStatus",
    "GetArticleReprintStatus",
    "GetArticleCommentStatus",
    "GetArticleHtml",
    "GetArticleText",
    "GetArticleMarkdown",
    "GetArticleCommentsData",
    "GetArticleAllBasicData",
    "GetArticleAllCommentsData",
]


def GetArticleTitle(article_url: str, disable_check: bool = False) -> str:
    """获取文章标题

    Args:
        article_url (str): 文章 URL
        disable_check (bool): 禁用参数有效性检查. Defaults to False.

    Returns:
        str: 文章标题
    """
    if not disable_check:
        AssertArticleUrl(article_url)
        AssertArticleStatusNormal(article_url)
    json_obj = GetArticleJsonDataApi(article_url)
    return json_obj["public_title"]


def GetArticleAuthorName(article_url: str, disable_check: bool = False) -> str:
    """获取文章作者名

    Args:
        article_url (str): 文章 URL
        disable_check (bool): 禁用参数有效性检查. Defaults to False.

    Returns:
        str: 文章作者名
    """
    if not disable_check:
        AssertArticleUrl(article_url)
        AssertArticleStatusNormal(article_url)
    json_obj = GetArticleHtmlJsonDataApi(article_url)
    return json_obj["props"]["initialState"]["note"]["data"]["user"]["nickname"]


def GetArticleReadsCount(article_url: str, disable_check: bool = False) -> int:
    """获取文章阅读量

    Args:
        article_url (str): 文章 URL
        disable_check (bool): 禁用参数有效性检查. Defaults to False.

    Returns:
        str: 文章阅读量
    """
    if not disable_check:
        AssertArticleUrl(article_url)
        AssertArticleStatusNormal(article_url)
    json_obj = GetArticleHtmlJsonDataApi(article_url)
    return json_obj["props"]["initialState"]["note"]["data"]["views_count"]


def GetArticleWordage(article_url: str, disable_check: bool = False) -> int:
    """获取文章字数

    Args:
        article_url (str): 文章 URL
        disable_check (bool): 禁用参数有效性检查. Defaults to False.

    Returns:
        str: 文章字数
    """
    if not disable_check:
        AssertArticleUrl(article_url)
        AssertArticleStatusNormal(article_url)
    json_obj = GetArticleHtmlJsonDataApi(article_url)
    return json_obj["props"]["initialState"]["note"]["data"]["wordage"]


def GetArticleLikesCount(article_url: str, disable_check: bool = False) -> int:
    """获取文章点赞量

    Args:
        article_url (str): 文章 URL
        disable_check (bool): 禁用参数有效性检查. Defaults to False.

    Returns:
        int: 文章点赞量
    """
    if not disable_check:
        AssertArticleUrl(article_url)
        AssertArticleStatusNormal(article_url)
    json_obj = GetArticleJsonDataApi(article_url)
    return json_obj["likes_count"]


def GetArticleCommentsCount(article_url: str, disable_check: bool = False) -> int:
    """获取文章评论数量

    Args:
        article_url (str): 文章 URL
        disable_check (bool): 禁用参数有效性检查. Defaults to False.

    Returns:
        int: 文章评论数量
    """
    if not disable_check:
        AssertArticleUrl(article_url)
        AssertArticleStatusNormal(article_url)
    json_obj = GetArticleJsonDataApi(article_url)
    return json_obj["public_comment_count"]


def GetArticleMostValuableCommentsCount(
    article_url: str, disable_check: bool = False
) -> int:
    """获取文章精选评论数量

    Args:
        article_url (str): 文章 URL
        disable_check (bool): 禁用参数有效性检查. Defaults to False.

    Returns:
        int: 文章精选评论数量
    """
    if not disable_check:
        AssertArticleUrl(article_url)
        AssertArticleStatusNormal(article_url)
    json_obj = GetArticleJsonDataApi(article_url)
    return json_obj["featured_comments_count"]


def GetArticleTotalFPCount(article_url: str, disable_check: bool = False) -> float:
    """获取文章总获钻量

    Args:
        article_url (str): 文章 URL
        disable_check (bool): 禁用参数有效性检查. Defaults to False.

    Returns:
        int: 文章总获钻量
    """
    if not disable_check:
        AssertArticleUrl(article_url)
        AssertArticleStatusNormal(article_url)
    json_obj = GetArticleJsonDataApi(article_url)
    return json_obj["total_fp_amount"] / 1000


def GetArticleDescription(article_url: str, disable_check: bool = False) -> str:
    """获取文章摘要

    Args:
        article_url (str): 文章 URL
        disable_check (bool): 禁用参数有效性检查. Defaults to False.

    Returns:
        str: 文章摘要
    """
    if not disable_check:
        AssertArticleUrl(article_url)
        AssertArticleStatusNormal(article_url)
    json_obj = GetArticleJsonDataApi(article_url)
    return json_obj["description"]


def GetArticlePublishTime(article_url: str, disable_check: bool = False) -> datetime:
    """获取文章发布时间

    Args:
        article_url (str): 文章 URL
        disable_check (str): 禁用参数有效性检查. Defaults to False.

    Returns:
        datetime: 文章发布时间
    """
    if not disable_check:
        AssertArticleUrl(article_url)
        AssertArticleStatusNormal(article_url)
    json_obj = GetArticleJsonDataApi(article_url)
    return datetime.fromisoformat(json_obj["first_shared_at"]).replace(tzinfo=None)


def GetArticleUpdateTime(article_url: str, disable_check: bool = False) -> datetime:
    """获取文章更新时间

    Args:
        article_url (str): 文章 URL
        disable_check (bool): 禁用参数有效性检查. Defaults to False.

    Returns:
        datetime: 文章更新时间
    """
    if not disable_check:
        AssertArticleUrl(article_url)
        AssertArticleStatusNormal(article_url)
    json_obj = GetArticleJsonDataApi(article_url)
    return datetime.fromtimestamp(json_obj["last_updated_at"])


def GetArticlePaidStatus(article_url: str, disable_check: bool = False) -> bool:
    """获取文章付费状态

    Args:
        article_url (str): 文章 URL
        disable_check (bool): 禁用参数有效性检查. Defaults to False.

    Returns:
        bool: 文章付费状态，True 为付费文章，False 为免费文章
    """
    if not disable_check:
        AssertArticleUrl(article_url)
        AssertArticleStatusNormal(article_url)
    json_obj = GetArticleJsonDataApi(article_url)
    paid_type = {
        "free": False,  # 免费文章
        "fbook_free": False,  # 免费连载中的免费文章
        "pbook_free": False,  # 付费连载中的免费文章
        "paid": True,  # 付费文章
        "fbook_paid": True,  # 免费连载中的付费文章
        "pbook_paid": True,  # 付费连载中的付费文章
    }
    return paid_type[json_obj["paid_type"]]


def GetArticleReprintStatus(article_url: str, disable_check: bool = False) -> bool:
    """获取文章转载声明状态

    Args:
        article_url (str): 文章 URL
        disable_check (bool): 禁用参数有效性检查. Defaults to False.

    Returns:
        bool: 文章转载声明状态，True 为允许转载，False 为禁止转载
    """
    if not disable_check:
        AssertArticleUrl(article_url)
        AssertArticleStatusNormal(article_url)
    json_obj = GetArticleJsonDataApi(article_url)
    return json_obj["reprintable"]


def GetArticleCommentStatus(article_url: str, disable_check: bool = False) -> bool:
    """获取文章评论区状态

    Args:
        article_url (str): 文章 URL
        disable_check (bool): 禁用参数有效性检查. Defaults to False.

    Returns:
        bool: 文章评论区状态，True 为开启评论，False 为关闭评论
    """
    if not disable_check:
        AssertArticleUrl(article_url)
        AssertArticleStatusNormal(article_url)
    json_obj = GetArticleJsonDataApi(article_url)
    return json_obj["commentable"]


def GetArticleHtml(article_url: str, disable_check: bool = False) -> str:
    """获取 Html 格式的文章内容

    # ! 该函数可以获取设置禁止转载的文章内容，请尊重作者版权，由此带来的风险您需自行承担
    # ! 该函数不能获取文章付费部分的内容

    Args:
        article_url (str): 文章 URL
        disable_check (bool): 禁用参数有效性检查. Defaults to False.

    Returns:
        str: Html 格式的文章内容
    """
    if not disable_check:
        AssertArticleUrl(article_url)
        AssertArticleStatusNormal(article_url)
    json_obj = GetArticleJsonDataApi(article_url)
    html_text = json_obj["free_content"]

    # 去除 image-container、image-container-fill 和 image-view
    html_text = sub(r'<div class="image-.*?" .*?>', "", html_text)
    # 去除 image-package
    html_text = html_text.replace('<div class="image-package">', "")

    old_img_blocks = findall(r"<img .*?>", html_text)  # 匹配旧的 img 标签
    if not old_img_blocks:  # 文章中没有图片块
        return html_text

    img_urls = [
        findall(r'<img data-original-src="(.*?)".*>', i)[0] for i in old_img_blocks
    ]
    new_img_blocks = [f'<img src="https:{img_url}">' for img_url in img_urls]

    for old_img_block, new_img_block in zip(old_img_blocks, new_img_blocks):
        html_text = html_text.replace(old_img_block, new_img_block)  # 替换 img 标签
    with open("result.html", "w", encoding="utf-8") as f:
        f.write(html_text)
    return html_text


def GetArticleText(article_url: str, disable_check: bool = False) -> str:
    """获取纯文本格式的文章内容

    # ! 该函数可以获取设置禁止转载的文章内容，请尊重作者版权，由此带来的风险您需自行承担
    # ! 该函数不能获取文章付费部分的内容

    Args:
        article_url (str): 文章 URL
        disable_check (bool): 禁用参数有效性检查. Defaults to False.

    Returns:
        str: 纯文本格式的文章内容
    """
    if not disable_check:
        AssertArticleUrl(article_url)
        AssertArticleStatusNormal(article_url)
    json_obj = GetArticleJsonDataApi(article_url)
    html_obj = etree.HTML(json_obj["free_content"])  # type: ignore
    result = "".join(html_obj.itertext())
    result = sub(r"\s{3,}", "", result)  # 去除多余的空行
    return result


def GetArticleMarkdown(article_url: str, disable_check: bool = False) -> str:
    """获取 Markdown 格式的文章内容

    # ! 该函数可以获取设置禁止转载的文章内容，请尊重作者版权，由此带来的风险您需自行承担
    # ! 该函数不能获取文章付费部分的内容

    Args:
        article_url (str): 文章 URL
        disable_check (bool): 禁用参数有效性检查. Defaults to False.

    Returns:
        str: Markdown 格式的文章内容
    """
    try:
        html2md  # noqa: B018  # type: ignore
    except NameError:
        raise ImportError("未安装 html2md 模块，该函数不可用") from None
    if not disable_check:
        AssertArticleUrl(article_url)
        AssertArticleStatusNormal(article_url)
    html_text = GetArticleHtml(article_url, disable_check=True)
    image_descriptions = list(
        findall(r'class="image-caption">.+</div>', html_text)
    )  # 获取图片描述块
    image_descriptions_text = [
        description.replace('class="image-caption">', "").replace("</div>", "")
        for description in findall(r'class="image-caption">.+</div>', html_text)
    ]  # 获取图片描述文本
    for index in range(len(image_descriptions)):
        html_text = html_text.replace(
            image_descriptions[index],
            "<p>&&" + image_descriptions_text[index] + "&&</p>",
        )  # 将图片描述替换成带有标记符的文本
    images = findall(r'<img src=".+">', html_text)  # 获取图片块
    for image in images:
        html_text = html_text.replace(image, f"<p>{image}</img></p>")  # 处理图片块
    markdown = html2md(html_text)  # 将 HTML 格式的文章转换成 Markdown 格式

    md_images_and_description = findall(
        r"!\[.*\]\(.+\)\n\n&&.+&&", markdown
    )  # 获取 Markdown 中图片语法和对应描述的部分
    md_images_url = [
        findall(r"https://.+\)", item)[0].replace(")", "")
        for item in md_images_and_description
    ]  # 获取所有图片链接
    md_image_descriptions = [
        findall(r"&&.+&&", item)[0].replace("&&", "")
        for item in md_images_and_description
    ]  # 获取所有图片描述

    for index, item in enumerate(md_images_and_description):
        markdown = markdown.replace(
            item, f"![{md_image_descriptions[index]}]({md_images_url[index]})"
        )  # 拼接 Markdown 语法并进行替换

    return markdown


def GetArticleCommentsData(
    article_id: int,
    page: int = 1,
    count: int = 10,
    author_only: bool = False,
    sorting_method: Literal["positive", "reverse"] = "positive",
) -> List[Dict]:
    """获取文章评论信息

    Args:
        article_id (int): 文章 ID
        page (int, optional): 页码. Defaults to 1.
        count (int, optional): 每次获取的评论数（不包含子评论）. Defaults to 10.
        author_only (bool, optional): 为 True 时只获取作者发布的评论，包含作者发布的子评论及其父评论. Defaults to False.
        sorting_method (Literal["positive", "reverse"], optional): 排序方式，为”positive“时按时间正序排列，为”reverse“时按时间倒序排列. Defaults to "positive".

    Returns:
        List[Dict]: 文章评论信息
    """
    order_by = {
        "positive": "asc",
        "reverse": "desc",
    }[sorting_method]
    json_obj = GetArticleCommentsJsonDataApi(
        article_id, page, count, author_only, order_by
    )
    result = []
    for item in json_obj["comments"]:
        item_data = {
            "cmid": item["id"],
            "publish_time": datetime.fromisoformat(item["created_at"]),
            "content": item["compiled_content"],
            "floor": item["floor"],
            "images": [image["url"] for image in item["images"]],
            "likes_count": item["likes_count"],
            "sub_comments_count": item["children_count"],
            "user": {
                "uid": item["user"]["id"],
                "name": item["user"]["nickname"],
                "uslug": item["user"]["slug"],
                "avatar_url": item["user"]["avatar"],
            },
        }
        try:
            item["user"]["member"]
        except KeyError:  # 没有开通会员
            pass
        else:
            item_data["user"]["vip_type"] = {
                "bronze": "铜牌",
                "silver": "银牌",
                "gold": "黄金",
                "platina": "白金",
                "ordinary": "普通（旧会员）",
                "distinguished": "至尊（旧会员）",
            }[item["user"]["member"]["type"]]
            item_data["user"]["vip_expire_date"] = datetime.fromtimestamp(
                item["user"]["member"]["expires_at"]
            )

        try:
            item["children"]
        except KeyError:  # 没有子评论
            pass
        else:
            item_data["sub_comments"] = []
            for sub_comment in item["children"]:
                sub_comment_data = {
                    "cmid": sub_comment["id"],
                    "publish_time": datetime.fromisoformat(sub_comment["created_at"]),
                    "content": sub_comment["compiled_content"],
                    "images": [image["url"] for image in sub_comment["images"]],
                    "parent_comment_id": sub_comment["parent_id"],
                    "user": {
                        "uid": sub_comment["user"]["id"],
                        "name": sub_comment["user"]["nickname"],
                        "uslug": sub_comment["user"]["slug"],
                        "avatar_url": sub_comment["user"]["avatar"],
                    },
                }

                try:
                    sub_comment["user"]["member"]
                except KeyError:  # 没有开通会员
                    pass
                else:
                    sub_comment_data["user"]["vip_type"] = {
                        "bronze": "铜牌",
                        "silver": "银牌",
                        "gold": "黄金",
                        "platina": "白金",
                        "ordinary": "普通（旧会员）",
                        "distinguished": "至尊（旧会员）",
                    }[sub_comment["user"]["member"]["type"]]
                    sub_comment_data["user"][
                        "vip_expire_date"
                    ] = datetime.fromtimestamp(
                        sub_comment["user"]["member"]["expires_at"]
                    )

                item_data["sub_comments"].append(sub_comment_data)

        result.append(item_data)
    return result


def GetArticleAllBasicData(article_url: str, disable_check: bool = False) -> Dict:
    """获取文章的全部基础信息

    Args:
        article_url (str): 文章 URL
        disable_check (bool): 禁用参数有效性检查. Defaults to False.

    Returns:
        Dict: 文章基础信息
    """
    if not disable_check:
        AssertArticleUrl(article_url)
        AssertArticleStatusNormal(article_url)
    result = {}
    json_obj = GetArticleJsonDataApi(article_url)
    html_json_obj = GetArticleHtmlJsonDataApi(article_url)

    result["title"] = json_obj["public_title"]
    result["author_name"] = html_json_obj["props"]["initialState"]["note"]["data"][
        "user"
    ]["nickname"]
    result["reads_count"] = html_json_obj["props"]["initialState"]["note"]["data"][
        "views_count"
    ]
    result["likes_count"] = json_obj["likes_count"]
    result["comments_count"] = json_obj["public_comment_count"]
    result["most_valuable_comments_count"] = json_obj["featured_comments_count"]
    result["wordage"] = html_json_obj["props"]["initialState"]["note"]["data"][
        "wordage"
    ]
    result["FP_count"] = json_obj["total_fp_amount"] / 1000
    result["description"] = json_obj["description"]
    result["publish_time"] = datetime.fromisoformat(json_obj["first_shared_at"])
    result["update_time"] = datetime.fromtimestamp(json_obj["last_updated_at"])
    result["paid_status"] = {
        "free": False,
        "fbook_free": False,
        "pbook_free": False,
        "paid": True,
        "fbook_paid": True,
        "pbook_paid": True,
    }[json_obj["paid_type"]]
    result["reprint_status"] = json_obj["reprintable"]
    result["comment_status"] = json_obj["commentable"]
    return result


def GetArticleAllCommentsData(
    article_id: int,
    count: int = 10,
    author_only: bool = False,
    sorting_method: Literal["positive", "reverse"] = "positive",
    max_count: Optional[int] = None,
) -> Generator[Dict, None, None]:
    """获取文章的全部评论信息

    Args:
        article_id (int): 文章 ID
        count (int, optional): 单次获取的数据数量，会影响性能. Defaults to 10.
        author_only (bool, optional): 为 True 时只获取作者发布的评论，包含作者发布的子评论及其父评论. Defaults to False.
        sorting_method (Literal["positive", "reverse"], optional): 排序方式，为”positive“时按时间正序排列，为”reverse“时按时间倒序排列. Defaults to "positive".
        max_count (int, optional): 获取的文章评论信息数量上限，Defaults to None.

    Yields:
        Iterator[Dict], None, None]: 文章信息
    """
    page = 1
    now_count = 0
    while True:
        result = GetArticleCommentsData(
            article_id, page, count, author_only, sorting_method
        )
        if result:
            page += 1
        else:
            return
        for item in result:
            yield item
            if max_count:
                now_count += 1
                if now_count == max_count:
                    return
