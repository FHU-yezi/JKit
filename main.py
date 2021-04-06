from .Basic import *
from .Errors import *

import json

import bs4
import requests

def GetUserID(user_url):
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

def GetFollowersCount(user_url):
    """该函数接收一个链接字符串，访问后提取用户的关注人数。

    Args:
        user_url (str): 链接字符串，需要加上 https

    Returns:
        int: 用户关注人数
    """
    html = requests.get(user_url,headers = UA)
    source = bs4.BeautifulSoup(html.content,parser)
    return int(source.findAll("div",class_ = "meta-block")[0].p.text)

def GetFansCount(user_url):
    """该函数接收一个链接字符串，访问后提取用户的粉丝数。

    Args:
        user_url (str): 链接字符串，需要加上 https

    Returns:
        int: 用户粉丝数
    """
    html = requests.get(user_url,headers = UA)
    source = bs4.BeautifulSoup(html.content,parser)
    return int(source.findAll("div",class_ = "meta-block")[1].p.text)

def GetArticlesCount(user_url):
    """该函数接收一个链接字符串，访问后提取用户的文章数。

    Args:
        user_url (str): 链接字符串，需要加上 https

    Returns:
        int: 用户文章数
    """
    html = requests.get(user_url,headers = UA)
    source = bs4.BeautifulSoup(html.content,parser)
    return int(source.findAll("div",class_ = "meta-block")[2].p.text)

def GetWordsCount(user_url):
    """该函数接收一个链接字符串，访问后提取用户的总字数。

    Args:
        user_url (str): 链接字符串，需要加上 https

    Returns:
        int: 用户总字数
    """
    html = requests.get(user_url,headers = UA)
    source = bs4.BeautifulSoup(html.content,parser)
    return int(source.findAll("div",class_ = "meta-block")[3].p.text)

def GetLikesCount(user_url):
    """该函数接收一个链接字符串，访问后提取用户被喜欢的总数。

    Args:
        user_url (str): 链接字符串，需要加上 https

    Returns:
        int: 用户被喜欢数（被点赞数）
    """
    html = requests.get(user_url,headers = UA)
    source = bs4.BeautifulSoup(html.content,parser)
    return int(source.findAll("div",class_ = "meta-block")[4].p.text)

def GetAssetsCount(user_url):
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
    return float(raw_data.replace(".","").replace("w","000"))

def GetUserBasicImformation(user_url):
    """该函数接收一个链接字符串，访问后提取用户的几项基础信息。

    Args:
        user_url (str): 链接字符串，需要加上 https

    Returns:
        str: 用户基础信息
    """
    html = requests.get(user_url,headers = UA)
    source = bs4.BeautifulSoup(html.content,parser)
    Name = "用户昵称：" + str(source.findAll("a",class_ = "name")[0].text)
    Followers = "关注数：" + str(source.findAll("div",class_ = "meta-block")[0].p.text)
    Fans = "粉丝数：" + str(source.findAll("div",class_ = "meta-block")[1].p.text)
    Articles ="文章数：" + str(source.findAll("div",class_ = "meta-block")[2].p.text)
    Words = "总字数：" + str(source.findAll("div",class_ = "meta-block")[3].p.text)
    Likes = "喜欢数：" + str(source.findAll("div",class_ = "meta-block")[4].p.text)
    Assets_temp = source.findAll("div",class_ = "meta-block")[5].p.text
    Assets = "总资产：" + str(Assets_temp.replace(".","").replace("w","000"))
    Item_List = [Name,"\n",Followers,"\n",Fans,"\n",Articles,"\n",Words,"\n",Likes,"\n",Assets]
    return "".join(Item_List)

def GetBadgesList(user_url):
    """该函数接收一个链接字符串，访问后提取用户的徽章列表。

    Args:
        user_url (str): 链接字符串，需要加上 https

    Returns:
        list: 用户被喜欢数（被点赞数）
    """
    html = requests.get(user_url,headers = UA)
    source = bs4.BeautifulSoup(html.content,parser)
    Item_List = []
    Final_List = []
    raw_data = source.findAll("li",class_ = "badge-icon")
    for raw_item in raw_data:
        Item_List.append(raw_item.find("a").text)
    for item in Item_List:
        Final_List.append(item.replace("\n","").replace(" ",""))
    return Final_List

def GetPersonalIntroduction(user_url):
    """该函数接收一个链接字符串，访问后提取用户个人简介。

    Args:
        user_url (str): 链接字符串，需要加上 https

    Returns:
        int: 用户个人简介
    """
    html = requests.get(user_url,headers = UA)
    source = bs4.BeautifulSoup(html.content,parser)
    raw_data = str(source.findAll("div",class_ = "js-intro")[0])
    return raw_data.replace('<div class="js-intro">',"").replace("<br/>","\n").replace("</div>","")

def GetUserNotebookInfo(user_url):
    """该函数接收一个用户主页链接，并获取该用户的文集与连载信息

    Args:
        user_url (str): 链接字符串，需要加上 https

    Returns:
        list: 包含用户文集与连载信息的列表
    """
    url = user_url.replace("/u/","/users/")
    id = GetUserID(user_url)
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

def GetUserFP(user_url):
    """该函数用于获取用户的简书钻数量

    Args:
        user_url (str): 链接字符串，需要加上 https

    Returns:
        float: 简书钻数量
    """
    html = requests.get(user_url,headers = Mobile_UA)
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
    Total_Assets = GetAssetsCount(user_url)
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
    for count in range(10):
        TradeInfo = []
        Trade = TradeList[count]
        TradeInfo.append(TradeList[count]["cantradenum"])
        TradeInfo.append(TradeList[count]["jianshuname"])
        TradeInfo.append(TradeList[count]["minlimit"])
        TradeInfo.append(TradeList[count]["nickname"])
        TradeInfo.append(TradeList[count]["recount"])
        TradeInfo.append(TradeList[count]["reprice"])
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
        output.append(ItemDict)
    return output

def GetBeiKeIslandTradePrice(Trade_type):
    """该函数用于获取贝壳小岛交易列表

    目前会返回前 10 条数据，买单为价格正序，卖单为价格倒序。

    Args:
        Trade_type (str): 为 buy 时返回买单列表，为 sell 时返回卖单列表。

    Returns:
        dict: 包含交易信息的字典
    """
    Raw_Data = GetBeiKeIslandTradeList(Trade_type)
    First_Dict = Raw_Data[0]
    return First_Dict["Price"]

def GetUserNoteTitleList(user_url,pages = 10000):
    """该函数用于获取用户的文章标题列表

    当不指定获取页码时，默认获取前 10000 页，基本等同于全部获取。

    Args:
        user_url (str): 链接字符串，需要加上 https
        pages (int, optional): 获取的页码数，默认为 10000

    Returns:
        list: 包含文章标题信息的列表
    """
    result_list = []
    for page in range(pages):
        list_len = len(result_list)
        page += 1
        url = user_url + "?order_by=shared_at&page=" + str(page)
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

def GetUserFollowersList(user_url,pages = 10000):
    raw_url = user_url.replace("/u/","/users/")
    raw_url = raw_url + "/following?page="
    result_list = []
    for page in range(pages):
        page = page + 1
        url = raw_url + str(page)
        print(url)
        html = requests.get(url + "1",headers = request_UA)
        source = bs4.BeautifulSoup(html.content,parser)
        data_list = source.findAll("a",class_ = "name")
        for item in data_list:
            result_list.append(item.text)
    return result_list

def GetAssetsRankList(start):
    """该函数接收一个起始值，并返回自起始值后 20 位用户的资产信息

    Args:
        start (int): 起始值

    Returns:
        list: 包含用户资产信息的列表
    """
    url = "https://www.jianshu.com/asimov/fp_rankings?max_id=1000000000&since_id=" + str(start)
    source = requests.get(url,headers = request_UA)
    source = json.loads(source.content)
    rank_list = source["rankings"]
    result_list = []
    for item in rank_list:
        info = {}
        info["ranking"] = item["ranking"]
        info["uid"] = item["user"]["id"]
        info["name"] = item["user"]["nickname"]
        info["assets"] = item["amount"]
        result_list.append(info)
    return result_list