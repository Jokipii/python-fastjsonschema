
import os
import sys
import importlib

from pprint import pprint

import pytest

from fastjsonschema import JsonSchemaException, compile, compile_to_code, _factory
from fastjsonschema.generator import CodeGenerator

current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(current_dir, os.pardir))


@pytest.fixture
def asserter():
    def f(definition, value, expected):
        # When test fails, it will show up code.
        resolver, code_generator = _factory(definition)
        print(code_generator.func_code)
        pprint(code_generator.global_state)

        validator = compile(definition)
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
        # When test fails, it will show up code.
        name, code = compile_to_code(definition)
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
