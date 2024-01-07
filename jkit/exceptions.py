class JKitError(Exception):
    pass


class ValidationError(Exception):
    pass


class APIUnsupportedError(JKitError):
    pass


class ResourceUnavailableError(JKitError):
    pass


class AssetsActionError(JKitError):
    pass


class BalanceNotEnoughError(AssetsActionError):
    pass


class WeeklyConvertLimitExceededError(AssetsActionError):
    pass
