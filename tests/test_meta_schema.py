from types import FunctionType

import pytest

from fastjsonschema import Config, compile, JsonSchemaException


@pytest.mark.parametrize('value, draft, expected', [
    ({'type': 'integer'}, 'draft4', FunctionType),
    ({'type': 'integer', 'exclusiveMinimum': True}, 'draft4', FunctionType),
    ({'type': 'integer', 'exclusiveMinimum': 0}, 'draft4', JsonSchemaException),
    ({'type': 'integer'}, 'draft6', FunctionType),
    ({'type': 'integer', 'exclusiveMinimum': 0}, 'draft6', FunctionType),
    ({'type': 'integer', 'exclusiveMinimum': True}, 'draft6', JsonSchemaException),
    ({'type': 'integer', 'exclusiveMinimum': 0}, 'draft7', FunctionType),
    ({'type': 'integer', 'exclusiveMinimum': True}, 'draft7', JsonSchemaException),

])
def test_meta_schema(value, draft, expected):
    config = Config(schema_version=draft, validate_schema=True)
    try:
        func = compile(value, config=config)
    except JsonSchemaException:
        assert expected == JsonSchemaException
    else:
        assert isinstance(func, expected)
