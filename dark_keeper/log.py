import logging
import os

from .storage import Storage


def get_log(log_format='%(asctime)s %(message)s', log_file=None):
    if log_file:
        Storage.create_dirs(os.path.dirname(log_file))

    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter(log_format)

    # fix double output
    log.handlers = []

    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        log.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)

    return log
