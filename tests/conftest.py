
import os
import sys
import importlib
from pprint import pprint

import requests
import pytest

from fastjsonschema import JsonSchemaException, compile, compile_to_code, _factory
from fastjsonschema.generator import CodeGenerator
from fastjsonschema.config import Config

current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(current_dir, os.pardir))


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


CONFIG = Config(
    meta_schema='draft4',
    uri_handlers={'http': remotes_handler},
    validate_schema=False,
)


@pytest.fixture
def asserter():
    def f(definition, value, expected):
        config = Config(meta_schema='draft4')
        # When test fails, it will show up code.
        resolver, code_generator = _factory(definition, config=CONFIG)
        print(code_generator.code)

        validator = compile(definition, config=CONFIG)
        if isinstance(expected, JsonSchemaException):
            with pytest.raises(JsonSchemaException) as exc:
                validator(value)
            assert exc.value.message == expected.message
        else:
            assert validator(value) == expected
    return f


@pytest.fixture
def asserter_cc():
    def f(definition, value, expected, filename):
        config = Config(meta_schema='draft4', validate_schema=False)
        # When test fails, it will show up code.
        name, code = compile_to_code(definition, config=CONFIG)
        print(code)

        if not os.path.isdir('temp'):
            os.makedirs('temp')
        with open('temp/' + filename + '.py', 'w') as f:
            f.write(code)
        validator = getattr(importlib.import_module('temp.' + filename), name)
        if isinstance(expected, JsonSchemaException):
            with pytest.raises(JsonSchemaException) as exc:
                validator(value)
            assert exc.value.message == expected.message
        else:
            assert validator(value) == expected
    return f
