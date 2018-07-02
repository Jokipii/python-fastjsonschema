import pytest

from fastjsonschema import JsonSchemaException, compile_to_code


exc = JsonSchemaException('data.a must be string')
@pytest.mark.parametrize('value, expected', [
    ({'a': 'a', 'b': 1}, {'a': 'a', 'b': 1}),
    ({'a': 1, 'b': 1}, exc),
])
def test_compile_to_code(asserter_cc, value, expected):
    asserter_cc(
        {'properties': {
            'a': {'type': 'string'},
            'b': {'type': 'integer'},
        }}, value, expected
    )

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
