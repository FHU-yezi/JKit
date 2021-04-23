# 如果在外部导入本模块，会触发 try 块中的代码，实现相对导入
# 如果直接运行本模块，ImportError 异常会自动被捕获，并使用另一种导入方式

try:
    from .Basic import *
    from .Errors import *
except ImportError:
    from Basic import *
    from Errors import *

import json

import bs4
import requests

def GetUID(user_url):
    """该函数接收一个链接字符串，并将其转换成用户识别码。

    Args:
        user_url (str):链接字符串，需要加上 https
    
    Returns:
        str: 用户识别码
    """
    return user_url.replace("https://www.jianshu.com/u/","")

def GetUserURL(user_ID):
    """该函数接收用户 ID，并将其转换成用户主页链接。

    Args:
        user_ID (str): 一个 12 位字符串

    Returns:
        str: 用户个人主页链接
    """
    return "https://www.jianshu.com/u/" + user_ID

def GetUserName(user_url):
    """该函数接收一个链接字符串，访问后提取用户昵称。

    Args:
        user_url (str): 链接字符串，需要加上 https

    Returns:
        str: 用户昵称
    """
    html = requests.get(user_url,headers = UA)
    source = bs4.BeautifulSoup(html.content,parser)
    return source.findAll("a",class_ = "name")[0].text

def GetUserFollowersCount(user_url):
    """该函数接收一个链接字符串，访问后提取用户的关注人数。

    Args:
        user_url (str): 链接字符串，需要加上 https

    Returns:
        int: 用户关注人数
    """
    html = requests.get(user_url,headers = UA)
    source = bs4.BeautifulSoup(html.content,parser)
    return int(source.findAll("div",class_ = "meta-block")[0].p.text)

def GetUserFansCount(user_url):
    """该函数接收一个链接字符串，访问后提取用户的粉丝数。

    Args:
        user_url (str): 链接字符串，需要加上 https

    Returns:
        int: 用户粉丝数
    """
    html = requests.get(user_url,headers = UA)
    source = bs4.BeautifulSoup(html.content,parser)
    return int(source.findAll("div",class_ = "meta-block")[1].p.text)

def GetUserArticlesCount(user_url):
    """该函数接收一个链接字符串，访问后提取用户的文章数。

    Args:
        user_url (str): 链接字符串，需要加上 https

    Returns:
        int: 用户文章数
    """
    html = requests.get(user_url,headers = UA)
    source = bs4.BeautifulSoup(html.content,parser)
    return int(source.findAll("div",class_ = "meta-block")[2].p.text)

def GetUserWordsCount(user_url):
    """该函数接收一个链接字符串，访问后提取用户的总字数。

    Args:
        user_url (str): 链接字符串，需要加上 https

    Returns:
        int: 用户总字数
    """
    html = requests.get(user_url,headers = UA)
    source = bs4.BeautifulSoup(html.content,parser)
    return int(source.findAll("div",class_ = "meta-block")[3].p.text)

def GetUserLikesCount(user_url):
    """该函数接收一个链接字符串，访问后提取用户被喜欢的总数。

    Args:
        user_url (str): 链接字符串，需要加上 https

    Returns:
        int: 用户被喜欢数（被点赞数）
    """
    html = requests.get(user_url,headers = UA)
    source = bs4.BeautifulSoup(html.content,parser)
    return int(source.findAll("div",class_ = "meta-block")[4].p.text)

def GetUserAssetsCount(user_url):
    """该函数接收一个链接字符串，访问后提取用户资产量。

    当用户资产大于一定值时，网页中的显示值将以 w 为单位，本函数会对其自动进行处理，但无法突破其精确度限制。

    Args:
        user_url (str): 链接字符串，需要加上 https

    Returns:
        int: 用户资产量
    """
    html = requests.get(user_url,headers = UA)
    source = bs4.BeautifulSoup(html.content,parser)
    raw_data = source.findAll("div",class_ = "meta-block")[5].p.text
    return float(raw_data.replace(".","").replace("w","000")) # 处理资产大于一定值时的缩写

def GetUserBasicImformation(user_url):
    """该函数接收一个链接字符串，访问后提取用户的几项基础信息。

    Args:
        user_url (str): 链接字符串，需要加上 https

    Returns:
        dict: 用户基础信息
    """
    html = requests.get(user_url,headers = UA)
    source = bs4.BeautifulSoup(html.content,parser)
    result = {}
    result["name"] = source.findAll("a",class_ = "name")[0].text
    result["followers"] = source.findAll("div",class_ = "meta-block")[0].p.text
    result["fans"] = source.findAll("div",class_ = "meta-block")[1].p.text
    result["articles"] = source.findAll("div",class_ = "meta-block")[2].p.text
    result["words"] = source.findAll("div",class_ = "meta-block")[3].p.text
    result["likes"] = source.findAll("div",class_ = "meta-block")[4].p.text
    Assets_temp = source.findAll("div",class_ = "meta-block")[5].p.text
    result["total_assets"] = Assets_temp.replace(".","").replace("w","000")
    return result

def GetUserBadgesList(user_url):
    """该函数接收一个链接字符串，访问后提取用户的徽章列表。

    Args:
        user_url (str): 链接字符串，需要加上 https

    Returns:
        list: 用户徽章列表
    """
    html = requests.get(user_url,headers = UA)
    source = bs4.BeautifulSoup(html.content,parser)
    Item_List = []
    Final_List = []
    raw_data = source.findAll("li",class_ = "badge-icon")
    for raw_item in raw_data:
        Item_List.append(raw_item.find("a").text)
    for item in Item_List:
        Final_List.append(item.replace(" ","").replace("\n","")) # 去除空格和换行符
    return Final_List

def GetUserIntroduction(user_url):
    """该函数接收一个链接字符串，访问后提取用户个人简介。

    Args:
        user_url (str): 链接字符串，需要加上 https

    Returns:
        int: 用户个人简介
    """
    html = requests.get(user_url,headers = UA)
    source = bs4.BeautifulSoup(html.content,parser)
    raw_data = str(source.findAll("div",class_ = "js-intro")[0])
    # 不知为何无法直接获取到简介字段，只能退而求其次获取上层字段再进行替换
    # 如果用户简介中含有被替换的字符，会导致结果错误
    # TODO:使用直接提取字段的方式重写本函数，避免可能造成的结果错误
    return raw_data.replace('<div class="js-intro">',"").replace("<br/>","\n").replace("</div>","")

def GetUserNotebookInfo(user_url):
    """该函数接收一个用户主页链接，并获取该用户的文集与连载信息

    Args:
        user_url (str): 链接字符串，需要加上 https

    Returns:
        list: 包含用户文集与连载信息的列表
    """
    url = user_url.replace("/u/","/users/")
    id = GetUID(user_url)
    url = url + "/collections_and_notebooks?slug=" + id
    source = requests.get(url,headers = request_UA)
    source = json.loads(source.content)
    result_list = []
    Notebook_List = source["notebooks"]
    for item in Notebook_List:
        info = {}
        info["nid"] = item["id"]
        info["name"] = item["name"]
        info["is_book"] = item["book"]
        if item["book"] == True:
            info["paid_book"] = item["paid_book"] # 如果是连载，则判断是否是付费连载
        result_list.append(info)
    return result_list

def GetUserManageableCollectionInfo(user_url):
    """该函数接收用户链接，并返回该用户拥有管理权的专题信息

    Args:
        user_url (str): 链接字符串，需要加上 https

    Returns:
        dict: 拥有管理权的专题信息
    """
    url = user_url.replace("/u/","/users/")
    id = GetUID(user_url)
    url = url + "/collections_and_notebooks?slug=" + id
    source = requests.get(url,headers = request_UA)
    source = json.loads(source.content)
    result_list = []
    Collcetion_List = source["manageable_collections"]
    for item in Collcetion_List:
        info = {}
        info["cid"] = item["id"]
        info["name"] = item["title"]
        result_list.append(info)
    return result_list

def GetUserOwnCollectionInfo(user_url):
    """该函数接收用户链接，并返回该用户自己创建的专题信息

    Args:
        user_url (str): 链接字符串，需要加上 https

    Returns:
        dict: 自己创建的专题信息
    """
    url = user_url.replace("/u/","/users/")
    id = GetUID(user_url)
    url = url + "/collections_and_notebooks?slug=" + id
    source = requests.get(url,headers = request_UA)
    source = json.loads(source.content)
    result_list = []
    Collcetion_List = source["own_collections"]
    for item in Collcetion_List:
        info = {}
        info["cid"] = item["id"]
        info["name"] = item["title"]
        result_list.append(info)
    return result_list

def GetBeiKeIslandTotalTradeAmount():
    """该函数用于获取贝壳小岛的总交易额。

    Returns:
        int: 总交易额
    """
    data = {"ranktype":3,"pageIndex":1}
    raw_data = requests.post("https://www.beikeisland.com/api/Trade/getTradeRankList",headers = BeiKeIslandHeaders,json = data)
    raw_data = json.loads(raw_data.content)
    return int((raw_data["data"]["totalcount"]))

def GetBeiKeIslandTotalTradeCount():
    """该函数用于获取贝壳小岛的总交易次数。

    Returns:
        int: 总交易次数
    """
    data = {"ranktype":3,"pageIndex":1}
    raw_data = requests.post("https://www.beikeisland.com/api/Trade/getTradeRankList",headers = BeiKeIslandHeaders,json = data)
    raw_data = json.loads(raw_data.content)
    return int((raw_data["data"]["totaltime"]))

def GetBeikeIslandTradeRanking(page = 1):
    """该函数接收一个页码参数，并返回贝壳小岛交易排行榜中的用户信息

    Args:
        page (int, optional): 页码参数，默认为 1

    Returns:
        list: 包含用户信息的列表
    """
    data = {"ranktype": 3, "pageIndex": page}
    raw_data = requests.post("https://www.beikeisland.com/api/Trade/getTradeRankList",headers = BeiKeIslandHeaders,json = data)
    raw_data = json.loads(raw_data.content)
    rank_list = raw_data["data"]["ranklist"]
    result_list = []
    for user in rank_list:
        info = {}
        info["bkuid"] = user["userid"]
        info["jianshuname"] = user["jianshuname"]
        info["amount"] = user["totalamount"]
        info["time"] = user["totaltime"]
        result_list.append(info)
    return result_list
        
def GetUserFP(user_url):
    """该函数用于获取用户的简书钻数量

    Args:
        user_url (str): 链接字符串，需要加上 https

    Returns:
        float: 简书钻数量
    """
    html = requests.get(user_url,headers = Mobile_UA) # 手机端网页会显示简书钻数量
    source = bs4.BeautifulSoup(html.content,parser)
    result = source.find("div",class_ = "follow-meta")
    result = result.findAll("span")[4].text
    result = result.replace("总资产","").replace(" ","").replace("\n","")
    return float(result)

def GetUserFTN(user_url):
    """该函数用于获取用户的简书贝数量

    由于该函数的实现方式利用了简书的已知漏洞，故有可能出现失效，这时代码会报错，避免数据错误。

    Args:
        user_url (str): 链接字符串，需要加上 https

    Returns:
        float: 简书贝数量
    """
    Total_Assets = GetUserAssetsCount(user_url)
    FP = GetUserFP(user_url)
    FTN = Total_Assets - FP
    if Total_Assets != 0 and FTN == 0:
        raise MethodError("Total Assets is not 0, but FTN is 0, maybe the method has some errors.")
    return round(FTN,2)

def GetBeiKeIslandTradeList(Trade_type):
    """该函数用于获取贝壳小岛交易列表

    目前会返回前 10 条数据，买单为价格正序，卖单为价格倒序。

    Args:
        Trade_type (str): 为 buy 时返回买单列表，为 sell 时返回卖单列表。

    Returns:
        dict: 包含交易信息的字典
    """
    if Trade_type == "buy":
        Trade_type = 2
    elif Trade_type == "sell":
        Trade_type = 1
    else:
        raise ValueError("Wrong parameter")
    output = []
    data = {"pageIndex":1,"retype":Trade_type}
    raw_data = requests.post("https://www.beikeisland.com/api/Trade/getTradeList",headers = BeiKeIslandHeaders,json = data)
    raw_data = json.loads(raw_data.content)
    TradeList = raw_data["data"]["tradelist"]
    FinalData = {}
    # TODO:重写这段屎山代码
    for count in range(10):
        TradeInfo = []
        Trade = TradeList[count]
        TradeInfo.append(TradeList[count]["cantradenum"])
        TradeInfo.append(TradeList[count]["jianshuname"])
        TradeInfo.append(TradeList[count]["minlimit"])
        TradeInfo.append(TradeList[count]["nickname"])
        TradeInfo.append(TradeList[count]["recount"])
        TradeInfo.append(TradeList[count]["reprice"])
        TradeInfo.append(TradeList[count]["userlevel"])
        FinalData[count] = TradeInfo
    for count in range(10):
        Trade = FinalData[count]
        ItemDict = {}
        ItemDict["JianshuName"] = Trade[1]
        ItemDict["BeiKeIslandName"] = Trade[3]
        ItemDict["Total"] = Trade[4]
        ItemDict["Remaining"] = Trade[0]
        ItemDict["TradeLimit"] = Trade[2]
        ItemDict["Price"] = Trade[5]
        ItemDict["UserLevel"] = Trade[6]
        output.append(ItemDict)
    return output

def GetBeiKeIslandTradePrice(Trade_type):
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

def GetUserNoteTitleList(user_url,pages = 1):
    """该函数用于获取用户的文章标题列表

    Args:
        user_url (str): 链接字符串，需要加上 https
        pages (int, optional): 获取的页码数，默认为 1

    Returns:
        list: 包含文章标题信息的列表
    """
    result_list = []
    for page in range(pages):
        list_len = len(result_list)
        page += 1
        url = user_url + "?page=" + str(page)
        html = requests.get(url,headers = request_UA)
        source = bs4.BeautifulSoup(html.content,parser)
        Note_List = source.findAll("li")
        for note in Note_List:
            note = note.find("div",class_ = "content")
            result = note.find("a",class_ = "title").text
            result_list.append(result)
        if list_len == len(result_list):
            break
    return result_list

def GetUserFollowersList(user_url,pages = 1):
    """该函数接收用户链接，并返回该用户的关注列表

    Args:
        user_url (str): 链接字符串，需要加上 https
        pages (int, optional): 获取的页码数，默认为 1

    Returns:
        list: 包含用户关注信息的列表
    """
    raw_url = user_url.replace("/u/","/users/")
    raw_url = raw_url + "/following?page="
    result_list = []
    for page in range(pages):
        page = page + 1
        url = raw_url + str(page)
        print(url)
        html = requests.get(url,headers = request_UA)
        source = bs4.BeautifulSoup(html.content,parser)
        data_list = source.findAll("a",class_ = "name")
        for item in data_list:
            result_list.append(item.text)
    return result_list

def GetUserFansList(user_url,pages = 1):
    """该函数接收用户链接，并返回该用户的粉丝列表

    Args:
        user_url (str): 链接字符串，需要加上 https
        pages (int, optional): 获取的页码数，默认为 1

    Returns:
        list: 包含用户粉丝信息的列表
    """
    raw_url = user_url.replace("/u/","/users/")
    raw_url = raw_url + "/followers?page="
    result_list = []
    for page in range(pages):
        page = page + 1
        url = raw_url + str(page)
        print(url)
        html = requests.get(url,headers = request_UA)
        source = bs4.BeautifulSoup(html.content,parser)
        data_list = source.findAll("a",class_ = "name")
        for item in data_list:
            result_list.append(item.text)
    return result_list

def GetAssetsRankList(start = 1):
    """该函数接收一个起始值，并返回自起始值后 20 位用户的资产信息

    Args:
        start (int): 起始值，默认为 1

    Returns:
        list: 包含用户资产信息的列表
    """
    start = start - 1
    url = "https://www.jianshu.com/asimov/fp_rankings?max_id=1000000000&since_id=" + str(start) # max_id 沿用了排行榜页面请求时的默认值
    source = requests.get(url,headers = request_UA)
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
        temp.insert(-3,".")
        temp = "".join(temp)
        info["assets"] = float(temp)
        result_list.append(info)
    return result_list

def GetArticleHtml(article_url):
    """该函数接收文章链接，并以 HTML 格式返回文章内容

    目前对图片块的处理还存在一些问题，会有多余的参数。

    Args:
        article_url (str): 文章链接

    Returns:
        str: HTML 格式的文章内容
    """
    # TODO:解决图片块的多余参数问题
    html = requests.get(article_url,headers = UA)
    source = bs4.BeautifulSoup(html.content,parser)
    raw_data = str(source.find("article"))
    result = Process_HTML(raw_data)
    return result

def GetArticleText(article_url):
    """该函数接收文章链接，并以纯文本格式返回文章内容

    文章中的图片块会被丢弃，但图片描述会保留

    Args:
        article_url (str): 文章链接

    Returns:
        str: 纯文本格式的文章内容
    """
    html = requests.get(article_url,headers = UA)
    source = bs4.BeautifulSoup(html.content,parser)
    result = str(source.find("article").text)
    result = result.replace("\n","")
    return result

def GetUserArticlesInfo(user_url,page = 1):
    url = user_url.replace("https://www.jianshu.com/u/","https://www.jianshu.com/asimov/users/slug/")
    url = url + "/public_notes?page=" + str(page) + "&count=10&order_by=shared_at"
    source = requests.get(url,headers = request_UA)
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
        info["fp_amount"] = item["total_fp_amount"]
        info["rewards_amount"] = item["total_rewards_count"]
        result_list.append(info)
    return result_list    

def GetDailyArticleRankList():
    """该函数返回日更排行榜中用户的基础信息

    Returns:
        list: 包含日更用户基础信息的列表
    """
    source = requests.get("https://www.jianshu.com/asimov/daily_activity_participants/rank",headers = request_UA)
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

def GetCollectionArticlesList(collcetion_url,page = 1):
    url = collcetion_url.replace("https://www.jianshu.com/c","https://www.jianshu.com/asimov/collections/slug")
    url = url + "/public_notes?page=" + str(page) + "&count=20&order_by=added_at"
    source = requests.get(url,headers = request_UA)
    source = json.loads(source.content)
    result_list = []
    for item in source:
        item_info = {}
        item = item["object"]["data"]
        item_info["title"] = item["title"]
        item_info["nid"] = item["id"]
        item_info["likes_count"] = item["likes_count"]
        item_info["time"] = item["first_shared_at"]
        item_info["commentable"] = item["commentable"]
        item_info["paid"] = item["paid"]
        item_info["topped"] = item["is_top"]
        item_info["comments_count"] = item["public_comments_count"]
        item_info["fp_amount"] = item["total_fp_amount"]
        item_info["rewards_count"] = item["total_rewards_count"]
        result_list.append(item_info)
    return result_list