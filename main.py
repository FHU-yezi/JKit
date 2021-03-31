from Basic import *
from Errors import *

import json

import bs4
import requests

def GetUserName(user_url):
    html = requests.get(user_url,headers = UA)
    source = bs4.BeautifulSoup(html.content,parser)
    return source.findAll("a",class_ = "name")[0].text

def GetFollowersCount(user_url):
    html = requests.get(user_url,headers = UA)
    source = bs4.BeautifulSoup(html.content,parser)
    return int(source.findAll("div",class_ = "meta-block")[0].p.text)

def GetFansCount(user_url):
    html = requests.get(user_url,headers = UA)
    source = bs4.BeautifulSoup(html.content,parser)
    return int(source.findAll("div",class_ = "meta-block")[1].p.text)

def GetArticlesCount(user_url):
    html = requests.get(user_url,headers = UA)
    source = bs4.BeautifulSoup(html.content,parser)
    return int(source.findAll("div",class_ = "meta-block")[2].p.text)

def GetWordsCount(user_url):
    html = requests.get(user_url,headers = UA)
    source = bs4.BeautifulSoup(html.content,parser)
    return int(source.findAll("div",class_ = "meta-block")[3].p.text)

def GetLikesCount(user_url):
    html = requests.get(user_url,headers = UA)
    source = bs4.BeautifulSoup(html.content,parser)
    return int(source.findAll("div",class_ = "meta-block")[4].p.text)

def GetAssetsCount(user_url):
    html = requests.get(user_url,headers = UA)
    source = bs4.BeautifulSoup(html.content,parser)
    raw_data = source.findAll("div",class_ = "meta-block")[5].p.text
    return float(raw_data.replace(".","").replace("w","000"))

def GetUserBasicImformation(user_url):
    Name = "用户昵称：" + str(GetUserName(user_url))
    Followers = "关注数：" + str(GetFollowersCount(user_url))
    Fans = "粉丝数：" + str(GetFansCount(user_url))
    Articles ="文章数：" + str(GetArticlesCount(user_url))
    Words = "总字数：" + str(GetWordsCount(user_url))
    Likes = "喜欢数：" + str(GetLikesCount(user_url))
    Assets = "总资产：" + str(GetAssetsCount(user_url))
    Item_List = [Name,"\n",Followers,"\n",Fans,"\n",Articles,"\n",Words,"\n",Likes,"\n",Assets]
    return "".join(Item_List)

def GetBadgesList(user_url):
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
    html = requests.get(user_url,headers = UA)
    source = bs4.BeautifulSoup(html.content,parser)
    raw_data = str(source.findAll("div",class_ = "js-intro")[0])
    return raw_data.replace('<div class="js-intro">',"").replace("<br/>","\n").replace("</div>","")

def GetBeiKeIslandTotalTradeAmount():
    data = {"ranktype":3,"pageIndex":1}
    raw_data = requests.post("https://www.beikeisland.com/api/Trade/getTradeRankList",headers = BeiKeIslandHeaders,json = data)
    raw_data = json.loads(raw_data.content)
    return int((raw_data["data"]["totalcount"]))

def GetBeiKeIslandTotalTradeCount():
    data = {"ranktype":3,"pageIndex":1}
    raw_data = requests.post("https://www.beikeisland.com/api/Trade/getTradeRankList",headers = BeiKeIslandHeaders,json = data)
    raw_data = json.loads(raw_data.content)
    return int((raw_data["data"]["totaltime"]))

def GetUserFP(user_url):
    html = requests.get(user_url,headers = Mobile_UA)
    source = bs4.BeautifulSoup(html.content,parser)
    result = source.find("div",class_ = "follow-meta")
    result = result.findAll("span")[4].text
    result = result.replace("总资产","").replace(" ","").replace("\n","")
    return float(result)

def GetUserFTN(user_url):
    Total_Assets = GetAssetsCount(user_url)
    FP = GetUserFP(user_url)
    FTN = Total_Assets - FP
    if Total_Assets != 0 and FTN == 0:
        raise MethodError("Total Assets is not 0, but FTN is 0, maybe the method has some errors.")
    return round(FTN,2)

def GetBeiKeIslandTradeList(Trade_type):
    if Trade_type == "buy":
        Trade_type = 2
    elif Trade_type == "sell":
        Trade_type = 1
    else:
        raise ValueError("Wrong parameter")
    headers = {"Host":"www.beikeisland.com",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57",
    "Content-Type":"application/json",
    "Version":"v2.0"}
    output = []
    data = {"pageIndex":1,"retype":Trade_type}
    raw_data = requests.post("https://www.beikeisland.com/api/Trade/getTradeList",headers = headers,json = data)
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
    Raw_Data = GetBeiKeIslandTradeList(Trade_type)
    First_Dict = Raw_Data[0]
    return First_Dict["Price"]

def GetUserNoteTitleList(user_url,pages = 10000):
    result_list = []
    for page in range(pages):
        list_len = len(result_list)
        page += 1
        url = user_url + "?order_by=shared_at&page=" + str(page)
        header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57",
        "X-INFINITESCROLL":"true",
        "X-Requested-With":"XMLHttpRequest"}
        html = requests.get(url,headers = header)
        source = bs4.BeautifulSoup(html.content,parser)
        Note_List = source.findAll("li")
        for note in Note_List:
            note = note.find("div",class_ = "content")
            result = note.find("a",class_ = "title").text
            result_list.append(result)
        if list_len == len(result_list):
            break
    return result_list
