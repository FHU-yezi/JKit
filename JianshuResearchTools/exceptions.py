__all__ = ["InputError", "APIError", "ResourceError"]


class InputError(Exception):
    """传入参数错误时抛出此异常
    """
    pass


class APIError(Exception):
    """API 受限导致无法获取信息时抛出此异常
    """
    pass


class ResourceError(Exception):
    """访问的资源状态异常时抛出此异常
    """
