import os

import pytest


@pytest.fixture
def log_files(export_dir):
    return [
        '',
        os.path.join(export_dir, 'export.log'),
        os.path.join(export_dir, 'export_two.log'),
        os.path.join(export_dir, 'not_exists', 'export.log'),
    ]


@pytest.fixture
def log_format():
    return '%(asctime)s %(message)s'
