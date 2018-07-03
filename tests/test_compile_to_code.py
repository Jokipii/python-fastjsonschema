import pytest

from fastjsonschema import JsonSchemaException, compile_to_code


exc = JsonSchemaException('data.a must be string')
@pytest.mark.parametrize('value, expected, filename', [
    ({'a': 'a', 'b': 1}, {'a': 'a', 'b': 1}, 'cc_test_1'),
    ({'a': 1, 'b': 1}, exc, 'cc_test_2'),
])
def test_compile_to_code(asserter_cc, value, expected, filename):
    asserter_cc(
        {'properties': {
            'a': {'type': 'string'},
            'b': {'type': 'integer'},
        }}, value, expected, filename
    )

exc = JsonSchemaException('data.a must match pattern [ab]')
@pytest.mark.parametrize('value, expected, filename', [
    ({'a': 'a', 'b': 1}, {'a': 'a', 'b': 1}, 'cc_test_3'),
    ({'a': 'c', 'b': 1}, exc, 'cc_test_4'),
])
def test_compile_to_code_with_regex(asserter_cc, value, expected, filename):
    asserter_cc(
        {
            'properties': {
                'a': {'type': 'string', 'pattern': '[ab]'},
                'b': {'type': 'integer'},
            }
        },
        value,
        expected,
        filename
    )
