__all__ = ["InputError", "APIError", "ResourceError"]


class InputError(Exception):
    """函数参数错误时抛出此异常"""

    pass


class APIError(Exception):
    """由于简书 API 受限导致无法获取数据时抛出此异常"""

    pass


class ResourceError(Exception):
    """访问的资源不存在或无法正常访问时抛出此异常"""
