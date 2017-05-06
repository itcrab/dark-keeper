import os
import sys

sys.path.append(
    os.path.join(os.path.dirname(__file__), 'fixtures')
)

pytest_plugins = [
    'fixtures_cache', 'fixtures_log', 'fixtures_menu', 'fixtures_parse',
    'fixtures_request', 'fixtures_storage'
]
