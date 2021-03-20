import bs4
import requests

from Errors import *
from Basic import *

def GetFollowersCount(user_url):
    html = requests.get(user_url,headers = UA)
    source = bs4.BeautifulSoup(html.content,parser)
    return int(source.find("div",class_ = "meta-block").p.text)

GetFollowersCount("https://www.jianshu.com/u/ea36c8d8aa30")