import pytest

from fastjsonschema import JsonSchemaException, compile_to_code
from fastjsonschema.generator import CodeGenerator
from fastjsonschema.ref_resolver import RefResolver


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


@pytest.mark.skip
@pytest.mark.benchmark(
    min_time=0.01,
    max_time=2,
    min_rounds=20,
    warmup=False
)
def test_bench_ref_resolver(benchmark):

    @benchmark
    def get_resolver():
        return RefResolver.from_schema(
            schema={
                'properties': {
                    'a': {'type': 'string', 'pattern': '[ab]'},
                    'b': {'type': 'integer'},
                }
            },
            schema_version='draft4',
            handlers={}
        )

    benchmark(get_resolver())


@pytest.mark.skip
@pytest.mark.benchmark(
    min_time=0.01,
    max_time=2,
    min_rounds=20,
    warmup=False
)
def test_bench_code_gen(benchmark):

    @benchmark
    def get_code_gen():
        resolver = RefResolver.from_schema(
            schema={
                'properties': {
                    'a': {'type': 'string', 'pattern': '[ab]'},
                    'b': {'type': 'integer'},
                }
            },
            schema_version='draft4',
            handlers={}
        )
        return CodeGenerator(resolver=resolver)

    benchmark(get_code_gen)
