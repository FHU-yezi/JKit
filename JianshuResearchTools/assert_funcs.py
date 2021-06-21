from errors import InputError


def AssertUserUrl(string: str) -> None:
    """该函数接收一个字符串，并在其不是有效的简书用户主页 Url 时抛出异常

    Args:
        string (str): 需要进行判断的字符串

    Raises:
        InputError: 意味着传入的参数不是有效的简书用户主页 Url
    """
    keyword_to_find = ["http", "www.jianshu.com", "/u/"]
    for keyword in keyword_to_find:
        if string.find(keyword) == -1:
            raise InputError("参数" + string + "不是有效的简书用户主页 Url")

def AssertArticleUrl(string: str) -> None:
    """该函数接收一个字符串，并在其不是有效的简书文章 Url 时抛出异常

    Args:
        string (str): 需要进行判断的字符串

    Raises:
        InputError: 意味着传入的参数不是有效的简书文章 Url
    """
    keyword_to_find = ["http", "www.jianshu.com", "/p/"]
    for keyword in keyword_to_find:
        if string.find(keyword) == -1:
            raise InputError("参数" + string + "不是有效的简书文章 Url")
        
def AssertCollectionUrl(string: str) -> None:
    """该函数接收一个字符串，并在其不是有效的简书专题 Url 时抛出异常

    Args:
        string (str): 需要进行判断的字符串

    Raises:
        InputError: 意味着传入的参数不是有效的简书专题 Url
    """
    keyword_to_find = ["http", "www.jianshu.com", "/c/"]
    for keyword in keyword_to_find:
        if string.find(keyword) == -1:
            raise InputError("参数" + string + "不是有效的简书专题 Url")

def AssertNotebookUrl(string: str) -> None:
    """该函数接收一个字符串，并在其不是有效的简书文集 Url 时抛出异常

    Args:
        string (str): 需要进行判断的字符串

    Raises:
        InputError: 意味着传入的参数不是有效的简书文集 Url
    """
    keyword_to_find = ["http", "www.jianshu.com", "/nb/"]
    for keyword in keyword_to_find:
        if string.find(keyword) == -1:
            raise InputError("参数" + string + "不是有效的简书文集 Url")

def AssertIslandUrl(string: str) -> None:
    """该函数接收一个字符串，并在其不是有效的简书小岛 Url 时抛出异常

    Args:
        string (str): 需要进行判断的字符串

    Raises:
        InputError: 意味着传入的参数不是有效的简书小岛 Url
    """
    keyword_to_find = ["http", "www.jianshu.com", "/g/"]
    for keyword in keyword_to_find:
        if string.find(keyword) == -1:
            raise InputError("参数" + string + "不是有效的简书小岛 Url")