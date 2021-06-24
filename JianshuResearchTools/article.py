import json
import re

import requests
from lxml import etree

from assert_funcs import AssertArticleUrl
from basic import jianshu_request_header


def GetArticleHtml(article_url: str) -> str:
    """该函数接收文章 Url，并以 HTML 格式返回文章内容

    # ! 该函数可以获取设置禁止转载的文章内容，请尊重作者版权，由此带来的风险由您自行承担
    # ! 该函数不能获取需要付费的文章内容
    # ! 文章中的图片描述将会丢失

    Args:
        article_url (str): 文章 Url

    Returns:
        str: HTML 格式的文章内容
    """
    AssertArticleUrl(article_url)
    request_url = article_url.replace("https://www.jianshu.com/", "https://www.jianshu.com/asimov/")
    source = requests.get(request_url, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    html_text = json_obj["free_content"]
    html_text = re.sub(r'\<div class="image-[\w]*" [ \w+-="]*>', "", html_text)  # 去除 image-view 和 image-container
    # TODO: 优化正则表达式，不去除 image-caption，即可保留图片描述
    html_text = re.sub(r'<div class=".+>', "", html_text)  # 去除 image-package、image-container-fill 和 image-caption
    old_img_blocks = re.findall(r'\<img[ \w+-="]*>', html_text)  # 匹配旧的 img 标签
    img_names = re.findall(r"\w+-\w+.[jpg | png]{3}",html_text)  # 获取图片名称
    new_img_blocks = ["".join(['<img src="https://upload-images.jianshu.io/upload_images/', \
                    img_name, '">']) for img_name in img_names]  # 拼接新的 img 标签
    for index in range(len(old_img_blocks)):
        if index == 0:
            replaced = html_text.replace(old_img_blocks[index], new_img_blocks[index])
        else:
            replaced = replaced.replace(old_img_blocks[index], new_img_blocks[index])  # 替换 img 标签
    return replaced
