import bs4
import requests

from Errors import *
from Basic import *

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
    return raw_data.replace(".","").replace("w","000")

