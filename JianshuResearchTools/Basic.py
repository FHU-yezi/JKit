UA = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
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

def AssertNoteURL(para):
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
