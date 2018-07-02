import os
import importlib
import pytest

from fastjsonschema import JsonSchemaException, compile_to_code


def test_compile_to_code():
    name, code = compile_to_code({
        'properties': {
            'a': {'type': 'string'},
            'b': {'type': 'integer'},
        }
    })
    if not os.path.isdir('temp'):
        os.makedirs('temp')
    with open('temp/schema.py', 'w') as f:
        f.write(code)
    validate = getattr(importlib.import_module('temp.schema'), name)
    assert validate({'a': 'a', 'b': 1}) == {'a': 'a', 'b': 1}

exc = JsonSchemaException('data.a must match pattern [ab]')
@pytest.mark.parametrize('value, expected', [
    ({'a': 'a', 'b': 1}, {'a': 'a', 'b': 1}),
    ({'a': 'c', 'b': 1}, exc),
])
def test_compile_to_code_with_regex(asserter_cc, value, expected):
    asserter_cc(
        {
            'properties': {
                'a': {'type': 'string', 'pattern': '[ab]'},
                'b': {'type': 'integer'},
            }
        },
        value,
        expected
    )
