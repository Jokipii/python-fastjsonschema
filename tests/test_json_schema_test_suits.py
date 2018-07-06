import json
import pytest
from pathlib import Path
import requests
from fastjsonschema import Config, CodeGenerator, RefResolver, JsonSchemaException, compile

REMOTES = {
    'http://localhost:1234/integer.json': {'type': 'integer'},
    'http://localhost:1234/name.json': {
        'type': 'string',
        'definitions': {
            'orNull': {'anyOf': [{'type': 'null'}, {'$ref': '#'}]},
        },
    },
    'http://localhost:1234/subSchemas.json': {
        'integer': {'type': 'integer'},
        'refToInteger': {'$ref': '#/integer'},
    },
    'http://localhost:1234/folder/folderInteger.json': {'type': 'integer'}
}

def remotes_handler(uri):
    print(uri)
    if uri in REMOTES:
        return REMOTES[uri]
    return requests.get(uri).json()


def resolve_param_values_and_ids(suite_dir, schema_version, ignored_suite_files, ignore_tests):

    suite_dir_path = Path(suite_dir).resolve()
    test_file_paths = sorted(set(suite_dir_path.glob("**/*.json")))

    param_values = []
    param_ids = []
    for test_file_path in test_file_paths:
        with test_file_path.open(encoding='UTF-8') as test_file:
            test_cases = json.load(test_file)
            for test_case in test_cases:
                for test_data in test_case['tests']:
                    param_values.append(pytest.param(
                        test_case['schema'],
                        schema_version,
                        test_data['data'],
                        test_data['valid'],
                        marks=pytest.mark.xfail
                            if test_file_path.name in ignored_suite_files
                                or test_case['description'] in ignore_tests
                            else pytest.mark.none,
                    ))
                    param_ids.append('{} / {} / {}'.format(
                        test_file_path.name,
                        test_case['description'],
                        test_data['description'],
                    ))
    return param_values, param_ids


def template_test(schema, schema_version, data, is_valid):
    config = Config(schema_version=schema_version, uri_handlers={'http': remotes_handler})
    # For debug purposes. When test fails, it will print stdout.
    resolver = RefResolver.from_schema(schema, config=config)
    print(CodeGenerator(resolver=resolver).func_code)

    validate = compile(schema, config)
    try:
        result = validate(data)
        print('Validate result:', result)
    except JsonSchemaException:
        if is_valid:
            raise
    else:
        if not is_valid:
            pytest.fail('Test should not pass')
