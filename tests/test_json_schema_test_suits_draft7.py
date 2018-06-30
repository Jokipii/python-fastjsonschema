import pytest
from test_json_schema_test_suits import template_test, resolve_param_values_and_ids

def pytest_generate_tests(metafunc):
    suite_dir = 'JSON-Schema-Test-Suite/tests/draft7'
    ignored_suite_files = [
        'ecmascript-regex.json',
        'content.json',
    ]
    ignore_tests = [
        'invalid definition',
        'valid definition',
        'validation of IRIs',
        'validation of time strings',
        'remote ref, containing refs itself',
        'items with boolean schema (false)',
        'contains keyword with const keyword',
    ]

    param_values, param_ids = resolve_param_values_and_ids(
        suite_dir, 'draft7', ignored_suite_files, ignore_tests
    )
    metafunc.parametrize(['schema', 'schema_version', 'data', 'is_valid'], param_values, ids=param_ids)

test = template_test
