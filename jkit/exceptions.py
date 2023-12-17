class JKitError(Exception):
    pass


class APIUnsupportedError(JKitError):
    pass


class ResourceUnavailableError(JKitError):
    pass
