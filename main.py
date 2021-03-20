import bs4
import requests

ua = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

def GetFollowersCount(user_url):
    html = requests.get(user_url,headers = ua)
    source = bs4.BeautifulSoup(html.content,"html.parser")
    return int(source.find("div",class_ = "meta-block").p.text)