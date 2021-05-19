__version__ = "1.3.0"

# 如果在外部导入本模块，会触发 try 块中的代码，实现相对导入
# 如果直接运行本模块，ImportError 异常会自动被捕获，并使用另一种导入方式

try:
    from .Basic import *
    from .Errors import *
except ImportError:
    from Basic import *
    from Errors import *

import json
import time
import re

import bs4
import requests


def GetUID(user_url: str) -> str:
    """该函数接收一个链接字符串，并将其转换成用户识别码。

    Args:
        user_url (str): 用户主页链接

    Returns:
        str: 用户识别码
    """
    AssertUserURL(user_url)
    return user_url.replace("https://www.jianshu.com/u/", "")


def GetUserURL(user_ID: str) -> str:
    """该函数接收用户 ID，并将其转换成用户主页链接。

    Args:
        user_ID (str): 一个 12 位字符串

    Returns:
        str: 用户个人主页链接
    """
    return "https://www.jianshu.com/u/" + user_ID


def GetUserName(user_url: str) -> str:
    """该函数接收一个链接字符串，访问后提取用户昵称。

    Args:
        user_url (str): 用户主页链接

    Returns:
        str: 用户昵称
    """
    AssertUserURL(user_url)
    html = requests.get(user_url, headers=UA)
    source = bs4.BeautifulSoup(html.content, parser)
    return source.findAll("a", class_="name")[0].text


def GetUserFollowersCount(user_url: str) -> int:
    """该函数接收一个链接字符串，访问后提取用户的关注人数。

    Args:
        user_url (str): 用户主页链接

    Returns:
        int: 用户关注人数
    """
    AssertUserURL(user_url)
    html = requests.get(user_url, headers=UA)
    source = bs4.BeautifulSoup(html.content, parser)
    return int(source.findAll("div", class_="meta-block")[0].p.text)


def GetUserFansCount(user_url: str) -> int:
    """该函数接收一个链接字符串，访问后提取用户的粉丝数。

    Args:
        user_url (str): 用户主页链接

    Returns:
        int: 用户粉丝数
    """
    AssertUserURL(user_url)
    html = requests.get(user_url, headers=UA)
    source = bs4.BeautifulSoup(html.content, parser)
    return int(source.findAll("div", class_="meta-block")[1].p.text)


def GetUserArticlesCount(user_url: str) -> int:
    """该函数接收一个链接字符串，访问后提取用户的文章数。

    Args:
        user_url (str): 用户主页链接

    Returns:
        int: 用户文章数
    """
    AssertUserURL(user_url)
    html = requests.get(user_url, headers=UA)
    source = bs4.BeautifulSoup(html.content, parser)
    return int(source.findAll("div", class_="meta-block")[2].p.text)


def GetUserWordsCount(user_url: str) -> int:
    """该函数接收一个链接字符串，访问后提取用户的总字数。

    Args:
        user_url (str): 用户主页链接

    Returns:
        int: 用户总字数
    """
    AssertUserURL(user_url)
    html = requests.get(user_url, headers=UA)
    source = bs4.BeautifulSoup(html.content, parser)
    return int(source.findAll("div", class_="meta-block")[3].p.text)


def GetUserLikesCount(user_url: str) -> int:
    """该函数接收一个链接字符串，访问后提取用户被喜欢的总数。

    Args:
        user_url (str): 用户主页链接
    Returns:
        int: 用户被喜欢数（被点赞数）
    """
    AssertUserURL(user_url)
    html = requests.get(user_url, headers=UA)
    source = bs4.BeautifulSoup(html.content, parser)
    return int(source.findAll("div", class_="meta-block")[4].p.text)


def GetUserAssetsCount(user_url: str) -> float:
    """该函数接收一个链接字符串，访问后提取用户资产量。

    当用户资产大于一定值时，网页中的显示值将以 w 为单位，本函数会对其自动进行处理，但无法突破其精确度限制。

    Args:
        user_url (str): 用户主页链接

    Returns:
        int: 用户资产量
    """
    AssertUserURL(user_url)
    html = requests.get(user_url, headers=UA)
    source = bs4.BeautifulSoup(html.content, parser)
    raw_data = source.findAll("div", class_="meta-block")[5].p.text
    # 处理资产大于一定值时的缩写
    return float(raw_data.replace(".", "").replace("w", "000"))


def GetUserBasicInformation(user_url: str) -> dict:
    """该函数接收一个链接字符串，访问后提取用户的基础信息。

    Args:
        user_url (str): 用户主页链接

    Returns:
        dict: 用户基础信息
    """
    AssertUserURL(user_url)
    html = requests.get(user_url, headers=UA)
    source = bs4.BeautifulSoup(html.content, parser)
    result = {}
    result["name"] = source.findAll("a", class_="name")[0].text
    result["followers"] = int(source.findAll("div", class_="meta-block")[0].p.text)
    result["fans"] = int(source.findAll("div", class_="meta-block")[1].p.text)
    result["articles"] = int(source.findAll("div", class_="meta-block")[2].p.text)
    result["words"] = int(source.findAll("div", class_="meta-block")[3].p.text)
    result["likes"] = int(source.findAll("div", class_="meta-block")[4].p.text)
    Assets_temp = source.findAll("div", class_="meta-block")[5].p.text
    result["total_assets"] = int(Assets_temp.replace(".", "").replace("w", "000"))
    return result


def GetUserBadgesList(user_url: str) -> list:
    """该函数接收一个链接字符串，访问后提取用户的徽章列表。

    Args:
        user_url (str): 用户主页链接

    Returns:
        list: 用户徽章列表
    """
    AssertUserURL(user_url)
    html = requests.get(user_url, headers=UA)
    source = bs4.BeautifulSoup(html.content, parser)
    Item_List = []
    Final_List = []
    raw_data = source.findAll("li", class_="badge-icon")
    for raw_item in raw_data:
        Item_List.append(raw_item.find("a").text)
    for item in Item_List:
        Final_List.append(item.replace(" ", "").replace("\n", ""))  # 去除空格和换行符
    return Final_List


def GetUserIntroduction(user_url: str) -> str:
    """该函数接收一个链接字符串，访问后提取用户个人简介。

    # ! 该函数在简介中有特殊字符的情况下可能出错，请知悉。

    Args:
        user_url (str): 用户主页链接

    Returns:
        int: 用户个人简介
    """
    AssertUserURL(user_url)
    html = requests.get(user_url, headers=UA)
    source = bs4.BeautifulSoup(html.content, parser)
    raw_data = str(source.findAll("div", class_="js-intro")[0])
    # 不知为何无法直接获取到简介字段，只能退而求其次获取上层字段再进行替换
    # 如果用户简介中含有被替换的字符，会导致结果错误
    # TODO:使用直接提取字段的方式重写本函数，避免可能造成的结果错误
    return raw_data.replace('<div class="js-intro">', "").replace("<br/>", "\n").replace("</div>", "")


def GetUserNotebookInfo(user_url: str) -> list:
    """该函数接收一个用户主页链接，并获取该用户的文集与连载信息

    Args:
        user_url (str): 用户主页链接

    Returns:
        list: 包含用户文集与连载信息的列表
    """
    AssertUserURL(user_url)
    url = user_url.replace("/u/", "/users/")
    id = GetUID(user_url)
    url = url + "/collections_and_notebooks?slug=" + id
    source = requests.get(url, headers=request_UA)
    source = json.loads(source.content)
    result_list = []
    Notebook_List = source["notebooks"]
    for item in Notebook_List:
        info = {}
        info["nid"] = item["id"]
        info["name"] = item["name"]
        info["is_book"] = item["book"]
        if item["book"] == True:
            info["paid_book"] = item["paid_book"]  # 如果是连载，则判断是否是付费连载
        result_list.append(info)
    return result_list


def GetUserManageableCollectionInfo(user_url: str) -> list:
    """该函数接收用户链接，并返回该用户拥有管理权的专题信息

    Args:
        user_url (str): 用户主页链接

    Returns:
        list: 拥有管理权的专题信息
    """
    AssertUserURL(user_url)
    url = user_url.replace("/u/", "/users/")
    id = GetUID(user_url)
    url = url + "/collections_and_notebooks?slug=" + id
    source = requests.get(url, headers=request_UA)
    source = json.loads(source.content)
    result_list = []
    Collection_List = source["manageable_collections"]
    for item in Collection_List:
        info = {}
        info["cid"] = item["id"]
        info["name"] = item["title"]
        result_list.append(info)
    return result_list


def GetUserOwnCollectionInfo(user_url: list) -> list:
    """该函数接收用户链接，并返回该用户自己创建的专题信息

    Args:
        user_url (str): 用户主页链接

    Returns:
        list: 自己创建的专题信息
    """
    AssertUserURL(user_url)
    url = user_url.replace("/u/", "/users/")
    id = GetUID(user_url)
    url = url + "/collections_and_notebooks?slug=" + id
    source = requests.get(url, headers=request_UA)
    source = json.loads(source.content)
    result_list = []
    Collection_List = source["own_collections"]
    for item in Collection_List:
        info = {}
        info["cid"] = item["id"]
        info["name"] = item["title"]
        result_list.append(info)
    return result_list


def GetBeiKeIslandTotalTradeAmount() -> int:
    """该函数用于获取贝壳小岛的总交易额。

    Returns:
        int: 总交易额
    """
    data = {"ranktype": 3, "pageIndex": 1}
    raw_data = requests.post("https://www.beikeisland.com/api/Trade/getTradeRankList", headers=BeiKeIslandHeaders, json=data)
    raw_data = json.loads(raw_data.content)
    return int(raw_data["data"]["totalcount"])


def GetBeiKeIslandTotalTradeCount() -> int:
    """该函数用于获取贝壳小岛的总交易次数。

    Returns:
        int: 总交易次数
    """
    data = {"ranktype": 3, "pageIndex": 1}
    raw_data = requests.post("https://www.beikeisland.com/api/Trade/getTradeRankList", headers=BeiKeIslandHeaders, json=data)
    raw_data = json.loads(raw_data.content)
    return int((raw_data["data"]["totaltime"]))


def GetBeikeIslandTradeRanking(page: int =1) -> list:
    """该函数接收一个页码参数，并返回贝壳小岛交易排行榜中的用户信息

    Args:
        page (int, optional): 页码参数，默认为 1

    Returns:
        list: 包含用户信息的列表
    """
    data = {"ranktype": 3, "pageIndex": page}
    raw_data = requests.post("https://www.beikeisland.com/api/Trade/getTradeRankList", headers=BeiKeIslandHeaders, json=data)
    raw_data = json.loads(raw_data.content)
    rank_list = raw_data["data"]["ranklist"]
    result_list = []
    for user in rank_list:
        info = {}
        info["bkuid"] = user["userid"]
        info["jianshuname"] = user["jianshuname"]
        info["amount"] = user["totalamount"]
        info["times"] = user["totaltime"]
        result_list.append(info)
    return result_list


def GetUserFP(user_url: str) -> float:
    """该函数用于获取用户的简书钻数量

    Args:
        user_url (str): 用户主页链接

    Returns:
        float: 简书钻数量
    """
    html = requests.get(user_url, headers=Mobile_UA) # 手机端网页会显示简书钻数量
    source = bs4.BeautifulSoup(html.content, parser)
    result = source.find("div", class_="follow-meta")
    result = result.findAll("span")[4].text
    result = result.replace("总资产", "").replace(" ", "").replace("\n", "")
    return float(result)


def GetUserFTN(user_url: str) -> float:
    """该函数用于获取用户的简书贝数量

    由于该函数的实现方式利用了简书的已知漏洞，故有可能出现失效，这时代码会报错，避免数据错误。

    Args:
        user_url (str): 用户主页链接

    Returns:
        float: 简书贝数量
    """
    AssertUserURL(user_url)
    Total_Assets = GetUserAssetsCount(user_url)
    FP = GetUserFP(user_url)
    FTN = Total_Assets - FP
    if Total_Assets != 0 and FTN == 0:
        raise MethodError("Total Assets is not 0, but FTN is 0, maybe the method has some errors.")
    return round(FTN, 2)


def GetBeiKeIslandTradeList(Trade_type: str) -> list:
    """该函数用于获取贝壳小岛交易列表

    目前会返回前 10 条数据，买单为价格正序，卖单为价格倒序。

    Args:
        Trade_type (str): 为 buy 时返回买单列表，为 sell 时返回卖单列表。

    Returns:
        list: 包含交易信息的列表
    """
    if Trade_type == "buy":
        Trade_type = 2
    elif Trade_type == "sell":
        Trade_type = 1
    else:
        raise ValueError("Wrong parameter")
    output = []
    data = {"pageIndex": 1, "retype": Trade_type}
    raw_data = requests.post("https://www.beikeisland.com/api/Trade/getTradeList", headers=BeiKeIslandHeaders, json=data)
    raw_data = json.loads(raw_data.content)
    TradeList = raw_data["data"]["tradelist"]
    FinalData = {}

    listdata = ["jianshuname",
                "nickname",
                "recount",
                "cantradenum",
                "minlimit",
                "reprice",
                "userlevel",
                ]
    listsavedata = ["JianshuName",
                    "BeiKeIslandName",
                    "Total",
                    "Remaining",
                    "TradeLimit",
                    "Price",
                    "UserLevel",
                    ]

    for count in range(10):
        TradeInfo = []
        Trade = TradeList[count]
        for data in listdata:
            TradeInfo.append(Trade[data])
        FinalData[count] = TradeInfo

    for count in range(10):
        Trade = FinalData[count]
        ItemDict = {}
        for sdata, i in zip(listsavedata, range(len(listdata))):
            ItemDict[sdata] = Trade[i]
        output.append(ItemDict)
    return output


def GetBeiKeIslandTradePrice(Trade_type: str) -> float:
    """该函数用于获取贝壳小岛的交易价格

    买单返回最低价，卖单返回最高价

    Args:
        Trade_type (str): 为 buy 时返回买单价格，为 sell 时返回卖单价格。

    Returns:
        float: 对应交易类型的价格
    """
    Raw_Data = GetBeiKeIslandTradeList(Trade_type)
    First_Dict = Raw_Data[0]
    return First_Dict["Price"]


def GetUserArticlesTitleList(user_url: str, pages: int =1) -> list:
    """该函数用于获取用户的文章标题列表

    Args:
        user_url (str): 用户主页链接
        pages (int, optional): 获取的页码数，默认为 1

    Returns:
        list: 包含文章标题信息的列表
    """
    AssertUserURL(user_url)
    result_list = []
    for page in range(pages):
        list_len = len(result_list)
        page += 1
        url = user_url + "?page=" + str(page)
        html = requests.get(url, headers=request_UA)
        source = bs4.BeautifulSoup(html.content, parser)
        Article_List = source.findAll("li")
        for article in Article_List:
            article = article.find("div", class_="content")
            result = article.find("a", class_="title").text
            result_list.append(result)
        if list_len == len(result_list):
            break
    return result_list


def GetUserFollowersList(user_url: str, pages: int =1) -> list:
    """该函数接收用户链接，并返回该用户的关注列表

    Args:
        user_url (str): 用户主页链接
        pages (int, optional): 获取的页码数，默认为 1

    Returns:
        list: 包含用户关注信息的列表
    """
    AssertUserURL(user_url)
    raw_url = user_url.replace("/u/", "/users/")
    raw_url = raw_url + "/following?page="
    result_list = []
    for page in range(pages):
        page = page + 1
        url = raw_url + str(page)
        html = requests.get(url, headers=request_UA)
        source = bs4.BeautifulSoup(html.content, parser)
        data_list = source.findAll("a", class_="name")
        for item in data_list:
            result_list.append(item.text)
    return result_list


def GetUserFansList(user_url: str, pages: int =1) -> list:
    """该函数接收用户链接，并返回该用户的粉丝列表

    Args:
        user_url (str): 用户主页链接
        pages (int, optional): 获取的页码数，默认为 1

    Returns:
        list: 包含用户粉丝信息的列表
    """
    AssertUserURL(user_url)
    raw_url = user_url.replace("/u/", "/users/")
    raw_url = raw_url + "/followers?page="
    result_list = []
    for page in range(pages):
        page = page + 1
        url = raw_url + str(page)
        html = requests.get(url, headers=request_UA)
        source = bs4.BeautifulSoup(html.content, parser)
        data_list = source.findAll("a", class_="name")
        for item in data_list:
            result_list.append(item.text)
    return result_list


def GetAssetsRankList(start: int=1) -> list:
    """该函数接收一个起始值，并返回自起始值后 20 位用户的资产信息

    Args:
        start (int): 起始值，默认为 1

    Returns:
        list: 包含用户资产信息的列表
    """
    start = start - 1
    url = "https://www.jianshu.com/asimov/fp_rankings?max_id=1000000000&since_id=" + str(start) # max_id 沿用了排行榜页面请求时的默认值
    source = requests.get(url, headers=request_UA)
    source = json.loads(source.content)
    rank_list = source["rankings"]
    result_list = []
    for item in rank_list:
        info = {}
        info["ranking"] = item["ranking"]
        info["uid"] = item["user"]["id"]
        info["slug"] = item["user"]["slug"]
        info["name"] = item["user"]["nickname"]
        temp = item["amount"]
        temp = list(str(temp))
        temp.insert(-3, ".")
        temp = "".join(temp)
        info["assets"] = float(temp)
        result_list.append(info)
    return result_list


def GetArticleHtml(article_url: str) -> str:
    """该函数接收文章链接，并以 HTML 格式返回文章内容

    目前对图片块的处理还存在一些问题，会有多余的参数。
    本函数无法获取文章中付费部分的内容。
    # !：本函数可以获取设置禁止转载的文章内容，请尊重版权，因违规转载造成的版权问题您需自行担责。

    Args:
        article_url (str): 文章链接

    Returns:
        str: HTML 格式的文章内容
    """
    # TODO:解决图片块的多余参数问题
    AssertArticleURL(article_url)
    url = article_url.replace("https://www.jianshu.com/", "https://www.jianshu.com/asimov/")
    source = requests.get(url, headers=request_UA).content
    source = json.loads(source)
    html = source["free_content"]
    return html


def GetArticleText(article_url: str) -> str:
    """该函数接收文章链接，并以纯文本格式返回文章内容

    文章中的图片块会被丢弃，但图片描述会保留。
    本函数无法获取文章中付费部分的内容。
    # !：本函数可以获取设置禁止转载的文章内容，请尊重版权，因违规转载造成的版权问题您需自行担责。

    Args:
        article_url (str): 文章链接

    Returns:
        str: 纯文本格式的文章内容
    """
    AssertArticleURL(article_url)
    url = article_url.replace("https://www.jianshu.com/", "https://www.jianshu.com/asimov/")
    source = requests.get(url, headers=request_UA).content
    source = json.loads(source)
    html = source["free_content"]
    source = bs4.BeautifulSoup(html, parser)
    result = source.text
    result = result.replace("\n", "")
    return result


def GetUserArticlesInfo(user_url: str, page: int =1) -> list:
    """该函数接收用户主页链接，并返回其文章的信息

    Args:
        user_url (str): 用户主页链接
        page (int, optional): 获取的页码数，默认为 1

    Returns:
        list: 包含用户文章信息的列表
    """
    AssertUserURL(user_url)
    url = user_url.replace("https://www.jianshu.com/u/","https://www.jianshu.com/asimov/users/slug/")
    url = url + "/public_notes?page=" + str(page) + "&count=10&order_by=shared_at"
    source = requests.get(url, headers=request_UA)
    source = json.loads(source.content)
    result_list = []
    for item in source:
        info = {}
        item = item["object"]["data"]
        info["title"] = item["title"]
        info["nid"] = item["id"]
        info["slug"] = item["slug"]
        info["time"] = item["first_shared_at"]
        info["views_count"] = item["views_count"]
        info["topped"] = item["is_top"]
        info["likes_count"] = item["likes_count"]
        info["paid"] = item["paid"]
        info["commentale"] = item["commentable"]
        info["comments_amount"] = item["public_comments_count"]
        info["fp_amount"] = item["total_fp_amount"] / 1000
        print(info["fp_amount"])
        info["rewards_amount"] = item["total_rewards_count"]
        result_list.append(info)
    return result_list


def GetDailyArticleRankList() -> list:
    """该函数返回日更排行榜中用户的基础信息

    Returns:
        list: 包含日更用户基础信息的列表
    """
    source = requests.get("https://www.jianshu.com/asimov/daily_activity_participants/rank", headers=request_UA)
    source = json.loads(source.content)
    raw_data = source["daps"]
    result_list = []
    for item in raw_data:
        info = {}
        info["ranking"] = item["rank"]
        info["days"] = item["checkin_count"]
        info["name"] = item["nickname"]
        info["slug"] = item["slug"]
        result_list.append(info)
    return result_list


def GetCollectionArticlesList(collection_url: str, page: int = 1) -> list:
    """该函数接收专题链接，并返回其中文章的信息

    Args:
        collertion_url (str): 专题链接
        page (int, optional): 获取的页码数，默认为 1

    Returns:
        list: 包含专题文章信息的列表
    """
    AssertCollectionURL(collection_url)
    url = collection_url.replace("https://www.jianshu.com/c", "https://www.jianshu.com/asimov/collections/slug")
    url = url + "/public_notes?page=" + str(page) + "&count=20&order_by=added_at"
    source = requests.get(url, headers=request_UA)
    source = json.loads(source.content)
    result_list = []

    listdatas = [
        "title",
        "id",
        "likes_count",
        "first_shared_at",
        "commentable",
        "paid",
        "public_comments_count",
        "total_fp_amount",
        "total_rewards_count",
        "slug"
    ]
    savelistdatas = [
        "title",
        "nid",
        "likes_count",
        "time",
        "commentable",
        "paid",
        "comments_count",
        "fp_amount",
        "rewards_count",
        "slug"
    ]

    for item in source:
        item_info = {}
        item = item["object"]["data"]
        for listdata, savelistdata in zip(listdatas, savelistdatas):
            item_info[f'{savelistdata}'] = item[f'{listdata}']
        result_list.append(item_info)
    return result_list


def GetArticleFPList(date: str ="latest") -> list:
    """该函数接收一个日期，并返回该日的文章收益排行榜数据

    Args:
        date (str, optional): 格式为”年月日“，如20210101

    Returns:
        list: 包含该日文章收益排行榜信息的列表
    """
    if date == "latest":
        date = time.strftime("%Y%m%d", time.localtime())
    url = "https://www.jianshu.com/asimov/fp_rankings/voter_notes?date=" + str(date)
    source = requests.get(url, headers=request_UA)
    source = json.loads(source.content)
    result = {}
    result["total_fp"] = source["fp"]
    result["total_fp_to_authors"] = source["author_fp"]
    result["total_fp_to_voters"] = source["fp"] - source["author_fp"]
    data = []
    for ranking, item in enumerate(source["notes"]):
        info = {}
        ranking = ranking + 1
        info["ranking"] = ranking
        info["article_title"] = item["title"]
        info["author_name"] = item["author_nickname"]
        info["author_slug"] = item["slug"]
        info["total_fp"] = item["fp"]
        info["fp_to_author"] = item["author_fp"]
        info["fp_to_voters"] = item["voter_fp"]
        data.append(info)
    result["data"] = data
    return data


def GetArticleTitle(article_url: str) -> str:
    """该函数接收文章链接，并返回该文章的标题

    Args:
        article_url (str): 文章链接

    Returns:
        str: 文章标题
    """
    AssertArticleURL(article_url)
    url = article_url.replace("https://www.jianshu.com/p/", "")
    url = "https://www.jianshu.com/asimov/p/" + url
    source = requests.get(url, headers=request_UA)
    source = json.loads(source.content)
    return source["public_title"]


def GetArticleID(article_url: str) -> str:
    """该函数接收文章链接，并返回该文章的 ID

    Args:
        article_url (str): 文章链接

    Returns:
        str: 文章 ID
    """
    AssertArticleURL(article_url)
    url = article_url.replace("https://www.jianshu.com/p/", "")
    url = "https://www.jianshu.com/asimov/p/" + url
    source = requests.get(url, headers=request_UA)
    source = json.loads(source.content)
    return str(source["id"])


def GetArticleLikeCount(article_url: str) -> int:
    """该函数接收文章链接，并返回该文章的点赞数

    Args:
        article_url (str): 文章链接

    Returns:
        int: 点赞数
    """
    AssertArticleURL(article_url)
    url = article_url.replace("https://www.jianshu.com/p/", "")
    url = "https://www.jianshu.com/asimov/p/" + url
    source = requests.get(url, headers=request_UA)
    source = json.loads(source.content)
    return source["likes_count"]


def GetArticleCommentCount(article_url: str) -> int:
    """该函数接收文章链接，并返回该文章的评论数

    Args:
        article_url (str): 文章链接

    Returns:
        int: 文章评论数
    """
    AssertArticleURL(article_url)
    url = article_url.replace("https://www.jianshu.com/p/", "")
    url = "https://www.jianshu.com/asimov/p/" + url
    source = requests.get(url, headers=request_UA)
    source = json.loads(source.content)
    return source["public_comment_count"]


def GetArticleFPCount(article_url: str) -> float:
    """该函数接收文章链接，并返回该文章的获钻数

    Args:
        article_url (str): 文章链接

    Returns:
        float: 文章获钻数
    """
    AssertArticleURL(article_url)
    url = article_url.replace("https://www.jianshu.com/p/", "")
    url = "https://www.jianshu.com/asimov/p/" + url
    source = requests.get(url, headers=request_UA)
    source = json.loads(source.content)
    result = source["total_fp_amount"]
    result = list(str(result))
    result.insert(-3, ".")
    result = "".join(result)
    result = float(result)
    return result


def GetArticlePublishTime(article_url: str) -> datetime:
    """该函数接收文章链接，并返回该文章的发布时间

    Args:
        article_url (str): 文章链接

    Returns:
        datetime: 文章发布时间（UTF+8）
    """
    AssertArticleURL(article_url)
    url = article_url.replace("https://www.jianshu.com/p/", "")
    url = "https://www.jianshu.com/asimov/p/" + url
    source = requests.get(url, headers=request_UA)
    source = json.loads(source.content)
    raw_text = source["first_shared_at"]
    result = StrToDatetime(raw_text)
    return result


def GetCollectionArticlesCount(collection_url: str) -> int:
    """该函数接收专题链接，并返回该专题内的文章数量

    Args:
        collection_url (str): 专题链接

    Returns:
        int: 专题中的文章数量
    """
    AssertCollectionURL(collection_url)
    html = requests.get(collection_url, headers=UA)
    source = bs4.BeautifulSoup(html.content, parser)
    result = source.findAll("div", class_="info")[0].text
    result = re.search("\d+", result).group(0)
    return result


def GetArticleCommentableStatus(article_url: str) -> bool:
    """该函数接收文章链接，并返回文章的评论区开启状态

    Args:
        article_url (url): 文章链接

    Returns:
        bool: 评论区开启状态
    """
    AssertArticleURL(article_url)
    url = article_url.replace("https://www.jianshu.com/p/", "https://www.jianshu.com/asimov/p/")
    source = requests.get(url, headers=request_UA)
    source = json.loads(source.content)
    return bool(source["commentable"])


def GetArticlePaidStatus(article_url: str) -> bool:
    """该函数接收文章链接，并返回文章的付费状态

    Args:
        article_url (str): 文章链接

    Returns:
        bool: 文章付费状态（有付费部分为 True，没有付费部分为 False）
    """
    AssertArticleURL(article_url)
    url = article_url.replace("https://www.jianshu.com/p/", "https://www.jianshu.com/asimov/p/")
    source = requests.get(url, headers=request_UA)
    source = json.loads(source.content)
    result = source["paid_type"]
    if result == "free":
        result = False
    elif result == "fbook_paid":
        result = True
    return result


def GetArticleReprintStatus(article_url: str) -> bool:
    """该函数接收文章链接，并返回文章的转载声明状态

    Args:
        article_url (str): 文章链接

    Returns:
        bool: 文章转载声明状态（可转载为 True，不可转载为 False）
    """
    AssertArticleURL(article_url)
    url = article_url.replace("https://www.jianshu.com/p/", "https://www.jianshu.com/asimov/p/")
    source = requests.get(url, headers=request_UA)
    source = json.loads(source.content)
    return bool(source["reprintable"])


def GetArticleSlug(article_url: str) -> str:
    """该函数接收一个文章 URL，并将其转换成文章 slug

    Args:
        article_url (str): 文章 URL

    Returns:
        str: 文章 slug
    """
    return article_url.replace("https://www.jianshu.com/p/","")

def GetIslandSlug(island_url: str) -> str:
    """该函数接收一个小岛 URL，并将其转换成小岛 slug

    Args:
        island_url (str): 小岛 URL

    Returns:
        str: 小岛 slug
    """
    return island_url.replace("https://www.jianshu.com/g/", "")

def GetIslandPostList(island_url: str, start_id: str=None, count:int=10, topic_id: str=None) -> list:
    """该函数接收一个小岛链接和一些可选参数，并返回小岛中帖子的基础信息

    Args:
        island_url (str): 小岛 URL
        max_id (str, optional): 起始帖子 ID，如不指定则获取最新的帖子。获取到的数据不包含这个 ID 对应的帖子. Defaults to None.
        count (int, optional): 获取的帖子个数. Defaults to 10.
        topic_id (str, optional): 话题 ID. Defaults to None.

    Returns:
        list: 包含小岛中帖子信息的列表
    """
    url = "https://www.jianshu.com/asimov/posts?group_slug=" + GetIslandSlug(island_url) + "&order_by=latest"
    if start_id != None:
        url = url + "&max_id=" + str(start_id)  # 万一用户传个整数呢
    url = url + "&count=" + str(count)
    if topic_id != None:
        url = url + "&topic_id=" + str(topic_id)
    source = requests.get(url, headers = request_UA)
    source = json.loads(source.content)

    result = []
    
    for item in source:
        item_data = {}
        item_data["sorted_id"] = str(item["sorted_id"])
        item_data["pid"] = str(item["id"])
        item_data["pslug"] = item["slug"]
        item_data["title"] = item["title"]
        item_data["content"] = item["content"]
        item_data["likes_count"] = item["likes_count"]
        item_data["comments_count"] = item["comments_count"]
        item_data["is_topped"] = item["is_top"]
        item_data["is_new"] = item["is_new"]
        item_data["is_hot"] = item["is_hot"]
        item_data["is_most_valuable"] = item["is_best"]
        item_data["create_time"] = time.localtime(item["created_at"])
        pic_list = []
        for pic in item["images"]:
            pic_list.append(pic["url"])
        item_data["pictures"] = pic_list
        item_data["nickname"] = item["user"]["nickname"]
        item_data["uid"] = str(item["user"]["id"])
        item_data["uslug"] = item["user"]["slug"]
        try:
            item_data["user_badge"] = item["user"]["badge"]["text"]
        except KeyError:
            pass  # 没有挂出徽章的跳过
        try:
            item_data["topic_name"] = item["topic"]["name"]
            item_data["tid"] = str(item["topic"]["id"])
            item_data["tslug"] = item["topic"]["slug"]
        except KeyError:
            pass  # 没有指定帖子话题的跳过
        result.append(item_data)
    return result

def GetUserPageURLScheme(user_url: str) -> str:
    """该函数接收一个用户主页 URL，返回跳转到简书 App 对应用户页面的 URL Scheme

    Args:
        user_url (str): 用户主页 URL

    Returns:
        str: 跳转到用户页面的 URL Scheme
    """
    AssertUserURL(user_url)
    return user_url.replace("https://www.jianshu.com/u/", "jianshu://u/")

def GetArticlePageURLScheme(article_url: str) -> str:
    """该函数接收一个文章 URL，返回跳转到简书 App 对应文章页面的 URL Scheme

    Args:
        article_url (str): 文章 URL

    Returns:
        str: 跳转到文章页面的 URL Scheme
    """
    AssertArticleURL(article_url)
    return article_url.replace("https://www.jianshu.com/p/", "jianshu://notes/")

def GetNotebookPageURLScheme(notebook_url: str) -> str:
    """该函数接收一个文集 URL，返回跳转到简书 App 对应文集页面的 URL Scheme

    Args:
        notebook_url (str): 文集 URL

    Returns:
        str: 跳转到文集页面的 URL Scheme
    """
    # TODO:补全检测是否是文集链接的函数
    return notebook_url.replace("https://www.jianshu.com/nb/", "jianshu://nb/")

def GetCollectionPageURLScheme(collection_url: str) -> str:
    """该函数接收一个专题 URL，返回跳转到简书 App 对应专题页面的 URL Scheme

    Args:
        collection_url (str): 专题 URL

    Returns:
        str: 跳转到专题页面的 URL Scheme
    """
    # TODO:补全检测是否是专题链接的函数
    return collection_url.replace("https://www.jianshu.com/c/", "jianshu://c/")