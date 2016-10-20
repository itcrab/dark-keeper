import logging
import os

from dark_keeper.log import get_log


def test_get_log(log_format):
    log = get_log(log_format)

    assert isinstance(log, logging.Logger)


def test_get_log_with_file(log_files, log_format):
    for log_file in log_files:
        log = get_log(log_format, log_file)

        assert isinstance(log, logging.Logger)

        if log_file:
            assert os.path.isfile(log_file)
