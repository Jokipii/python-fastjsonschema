import pytest
from test_json_schema_test_suits import template_test, resolve_param_values_and_ids

def pytest_generate_tests(metafunc):
    suite_dir = 'JSON-Schema-Test-Suite/tests/draft6'
    ignored_suite_files = [
        'bignum.json',
        'ecmascript-regex.json',
        'zeroTerminatedFloats.json',
        'boolean_schema.json',
        'contains.json',
        'const.json',
    ]
    ignore_tests = [
        'invalid definition',
        'valid definition',
        'remote ref, containing refs itself',
        'dependencies with boolean subschemas',
        'dependencies with empty array',
        'exclusiveMaximum validation',
        'exclusiveMinimum validation',
        'items with boolean schema (true)',
        'items with boolean schema (false)',
        'items with boolean schema',
        'items with boolean schemas',
        'not with boolean schema true',
        'not with boolean schema false',
        'properties with boolean schema',
        'propertyNames with boolean schema false',
        'propertyNames validation',
        'allOf with boolean schemas, all true',
        'allOf with boolean schemas, some false',
        'allOf with boolean schemas, all false',
        'anyOf with boolean schemas, all true',
        'anyOf with boolean schemas, some false',
        'anyOf with boolean schemas, all false',
        'anyOf with boolean schemas, some true',
        'oneOf with boolean schemas, all true',
        'oneOf with boolean schemas, some false',
        'oneOf with boolean schemas, all false',
        'oneOf with boolean schemas, one true',
        'oneOf with boolean schemas, more than one true',
        'patternProperties with boolean schemas',
        '$ref to boolean schema true',
        '$ref to boolean schema false',
    ]

    param_values, param_ids = resolve_param_values_and_ids(
        suite_dir, 'draft6', ignored_suite_files, ignore_tests
   )
    metafunc.parametrize(['schema', 'schema_version', 'data', 'is_valid'], param_values, ids=param_ids)

test = template_test
