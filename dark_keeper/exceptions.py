import math


class DarkKeeperError(Exception):
    pass


class DarkKeeperCacheError(DarkKeeperError):
    pass


class DarkKeeperCacheReadError(DarkKeeperCacheError):
    pass


class DarkKeeperParseError(DarkKeeperError):
    pass


class DarkKeeperParseHTMLError(DarkKeeperParseError):
    pass


class DarkKeeperRequestError(DarkKeeperError):
    pass


class DarkKeeperRequestResponseError(DarkKeeperRequestError):
    pass


class DarkKeeperStorageError(DarkKeeperError):
    pass


class DarkKeeperStorageExcelMaxLenStringError(DarkKeeperStorageError):
    def __init__(self, length, max_length, xls_strmax_mul):
        max_allowed = int(max_length / xls_strmax_mul)
        new_xls_strmax_mul = math.ceil(
            length / max_allowed
        )

        message = '''
Error: length of parsed row string is more than
max allowed ({max_allowed}) in Excel `{length} > {max_length}`

Hint: you need change `xls_strmax_mul` when
create `Storage` object
>>> ...
>>> xls_strmax_mul = {new_xls_strmax_mul}
>>> storage = Storage(model, export_dir, xls_strmax_mul)

this changes raised error (warning) in Excel but file
will be opened and you may see parsed data
'''.format(
            max_allowed=max_allowed,
            length=length, max_length=max_length,
            new_xls_strmax_mul=new_xls_strmax_mul
        )

        super().__init__(message)
