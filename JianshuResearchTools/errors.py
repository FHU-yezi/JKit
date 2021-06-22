class InputError(Exception):
    """该错误意味着传入的参数有误，如不是对应类型的 Url
    """
    pass

class NetWorkError(Exception):
    """该错误意味着在网络请求过程中发生了问题
    """
    pass

class APIException(Exception):
    """该错误意味着在函数内部的方法调用中出现了问题，一般与传入的参数无关
    """
    pass
