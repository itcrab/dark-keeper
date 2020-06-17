class DarkKeeperError(Exception):
    pass


class DarkKeeperCacheError(DarkKeeperError):
    pass


class DarkKeeperCacheReadError(DarkKeeperCacheError):
    pass


class DarkKeeperCacheWriteError(DarkKeeperCacheError):
    pass


class DarkKeeperParseError(DarkKeeperError):
    pass


class DarkKeeperParseContentError(DarkKeeperParseError):
    pass


class DarkKeeperRequestError(DarkKeeperError):
    pass


class DarkKeeperRequestResponseError(DarkKeeperRequestError):
    pass


class DarkKeeperMongoError(DarkKeeperError):
    pass


class DarkKeeperParseUriMongoError(DarkKeeperMongoError):
    pass
