import bs4
import datetime

UA = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
}

Mobile_UA = {
    "User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/89.0.4389.90"
}

request_UA = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57",
        "X-INFINITESCROLL":"true",
        "X-Requested-With":"XMLHttpRequest"}

BeiKeIslandHeaders = {"Host":"www.beikeisland.com",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57",
    "Content-Type":"application/json",
    "Version":"v2.0"}

parser = "html.parser"

def AssertUserURL(para):
    """该函数接收一个参数，并判断其是否是简书的用户主页 URL。

    Args:
        para (str): 需要被判断的参数

    Returns:
        bool: 如为 True 则代表是用户主页 URL，为 False 则不是
    """
    if para.find("http") == -1:
        return False
    if para.find("www.jianshu.com") == -1:
        return False
    if para.find("/u/") == -1:
        return False
    return True

def AssertArticleURL(para):
    """该函数接收一个参数，并判断其是否是简书的文章 URL。

    Args:
        para (str): 需要被判断的参数

    Returns:
        bool: 如为 True 则代表是文章 URL，为 False 则不是
    """
    if para.find("http") == -1:
        return False
    if para.find("www.jianshu.com") == -1:
        return False
    if para.find("/p/") == -1:
        return False
    return True

def Process_HTML(html):
    raw_html = bs4.BeautifulSoup(html,parser)
    result_html = []
    for item in raw_html:
        item = str(item)
        item = item.replace("<html><body>","")
        item = item.replace('<article class="_2rhmJa">',"")
        item = item.replace("</article>","")
        item = item.replace(' target="_blank"',"")
        result_html.append(item)
    result_html = "".join(result_html)
    return result_html

def StrToDatetime(text):
    """该函数接收一个由简书接口返回的字符串，并构建一个 Datetime 对象

    Args:
        text (str): 源字符串

    Returns:
        datetime: UTC+8，精确到秒
    """
    year = int(text[0:4])
    month = int(text[5:7])
    day = int(text[8:10])
    hour = int(text[11:13])
    minute = int(text[14:16])
    second = int(text[17:19])
    result = datetime.datetime(year,month,day,hour,minute,second)
    return result