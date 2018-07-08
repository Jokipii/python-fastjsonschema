import pytest

from fastjsonschema import JsonSchemaException, compile_to_code
from fastjsonschema.generator import CodeGenerator
from fastjsonschema.ref_resolver import RefResolver
from fastjsonschema.formats import FormatManager
from fastjsonschema.config import Config


from .conftest import CONFIG


EXC = JsonSchemaException('data.a must be string')
@pytest.mark.parametrize('value, expected, filename', [
    ({'a': 'a', 'b': 1}, {'a': 'a', 'b': 1}, 'cc_test_1'),
    ({'a': 1, 'b': 1}, EXC, 'cc_test_2'),
])
def test_compile_to_code(asserter_cc, value, expected, filename):
    asserter_cc(
        {'properties': {
            'a': {'type': 'string'},
            'b': {'type': 'integer'},
        }}, value, expected, filename
    )


EXC = JsonSchemaException('data.a must match pattern [ab]')
@pytest.mark.parametrize('value, expected, filename', [
    ({'a': 'a', 'b': 1}, {'a': 'a', 'b': 1}, 'cc_test_3'),
    ({'a': 'c', 'b': 1}, EXC, 'cc_test_4'),
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


@pytest.mark.benchmark(
    min_time=0.01,
    max_time=2,
    min_rounds=20,
    warmup=False
)
def test_bench_ref_resolver(benchmark):

    def get_resolver():
        return RefResolver.from_schema(
            schema={
                'properties': {
                    'a': {'type': 'string', 'pattern': '[ab]'},
                    'b': {'type': 'integer'},
                }
            },
            config=Config()
        )

    benchmark(get_resolver)


@pytest.mark.benchmark(
    min_time=0.01,
    max_time=2,
    min_rounds=20,
    warmup=False
)
def test_bench_code_gen(benchmark):

    current_resolver = RefResolver.from_schema(
        schema={
            'properties': {
                'a': {'type': 'string', 'pattern': '[ab]'},
                'b': {'type': 'integer'},
            }
        },
        config=Config()
    )
    format_manager = FormatManager()
    benchmark(CodeGenerator, resolver=current_resolver, formats=format_manager, config=CONFIG)
