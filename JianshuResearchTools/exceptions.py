class InputError(Exception):
    """该错误意味着传入的参数有误，如不是对应类型的 Url
    """
    pass

class APIError(Exception):
    """该错误意味着在函数内部的方法调用中出现了问题，一般与传入的参数无关
    """
    pass

class ResourceError(Exception):
    """该错误意味着访问的资源出现问题，如不存在或者审核中
    """