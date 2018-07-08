from textwrap import dedent
import timeit

# apt-get install jsonschema json-spec validictory
import fastjsonschema
import jsonschema
import validictory
from jsonspec.validators import load


NUMBER = 1000

JSON_SCHEMA = {
    'type': 'array',
    'items': [
        {
            'type': 'number',
            'maximum': 10,
            'exclusiveMaximum': True,
        },
        {
            'type': 'string',
            'enum': ['hello', 'world'],
        },
        {
            'type': 'array',
            'minItems': 1,
            'maxItems': 3,
            'items': [
                {'type': 'number'},
                {'type': 'string'},
                {'type': 'boolean'},
            ],
        },
        {
            'type': 'object',
            'required': ['a', 'b'],
            'minProperties': 3,
            'properties': {
                'a': {'type': ['null', 'string']},
                'b': {'type': ['null', 'string']},
                'c': {'type': ['null', 'string'], 'default': 'abc'}
            },
            'additionalProperties': {'type': 'string'},
        },
        {'not': {'type': ['null']}},
        {'oneOf': [
            {'type': 'number', 'multipleOf': 3},
            {'type': 'number', 'multipleOf': 5},
        ]},
    ],
}

VALUES_OK = (
    [9, 'hello', [1, 'a', True], {'a': 'a', 'b': 'b', 'd': 'd'}, 42, 3],
    [9, 'world', [1, 'a', True], {'a': 'a', 'b': 'b', 'd': 'd'}, 42, 3],
    [9, 'world', [1, 'a', True], {'a': 'a', 'b': 'b', 'c': 'xy'}, 42, 3],
    [9, 'world', [1, 'a', True], {'a': 'a', 'b': 'b', 'c': 'xy'}, 'str', 5],
)

VALUES_BAD = (
    [10, 'world', [1, 'a', True], {'a': 'a', 'b': 'b', 'c': 'xy'}, 'str', 5],
    [9, 'xxx', [1, 'a', True], {'a': 'a', 'b': 'b', 'c': 'xy'}, 'str', 5],
    [9, 'hello', [], {'a': 'a', 'b': 'b', 'c': 'xy'}, 'str', 5],
    [9, 'hello', [1, 2, 3], {'a': 'a', 'b': 'b', 'c': 'xy'}, 'str', 5],
    [9, 'hello', [1, 'a', True], {'a': 'a', 'x': 'x', 'y': 'y'}, 'str', 5],
    [9, 'hello', [1, 'a', True], {}, 'str', 5],
    [9, 'hello', [1, 'a', True], {'a': 'a', 'b': 'b', 'x': 'x'}, None, 5],
    [9, 'hello', [1, 'a', True], {'a': 'a', 'b': 'b', 'x': 'x'}, 42, 15],
)

def fast_file_not_comp(value, json_schema):
    with open('temp/speed.py', 'w') as fp:
        name, schema = fastjsonschema.compile_to_code(json_schema, config=config)
        fp.write(schema)
    from temp.speed import validate
    validate(value)

config = fastjsonschema.Config(schema_version='draft4')
fastjsonschema_validate = fastjsonschema.compile(JSON_SCHEMA, config=config)
fast_compiled = lambda value, _: fastjsonschema_validate(value)

fast_not_compiled = lambda value, json_schema: fastjsonschema.compile(json_schema, config=config)(value)

name, code = fastjsonschema.compile_to_code(JSON_SCHEMA, config=config)
with open('temp/performance.py', 'w') as f:
    f.write(code)
from temp.performance import validate
fast_file = lambda value, _: validate(value)

jsonspec = load(JSON_SCHEMA)
jsonschema_validator = jsonschema.Draft4Validator(JSON_SCHEMA)
jsonschema_compiled = lambda value, _: jsonschema_validator.validate(value)

def t(func, valid_values=True):
    module = func.split('.')[0]

    setup = """from __main__ import (
        JSON_SCHEMA,
        VALUES_OK,
        VALUES_BAD,
        validictory,
        jsonschema_compiled,
        jsonschema,
        jsonspec,
        fast_compiled,
        fast_file,
        fast_not_compiled,
        fast_file_not_comp,
    )
    """

    if valid_values:
        code = dedent("""
        for value in VALUES_OK:
            {}(value, JSON_SCHEMA)
        """.format(func))
    else:
        code = dedent("""
        try:
            for value in VALUES_BAD:
                {}(value, JSON_SCHEMA)
        except:
            pass
        """.format(func))

    res = timeit.timeit(code, setup, number=NUMBER)
    print('{:<25} {:<10} ==> {}'.format(module, 'valid' if valid_values else 'invalid', res))


print('Number: {}'.format(NUMBER))

t('fast_compiled')
t('fast_compiled', valid_values=False)

t('fast_file')
t('fast_file', valid_values=False)

t('jsonschema_compiled')
t('jsonschema_compiled', valid_values=False)

t('fast_file_not_comp')
t('fast_file_not_comp', valid_values=False)

t('fast_not_compiled')
t('fast_not_compiled', valid_values=False)

t('jsonschema.validate')
t('jsonschema.validate', valid_values=False)

t('jsonspec.validate')
t('jsonspec.validate', valid_values=False)

t('validictory.validate')
t('validictory.validate', valid_values=False)
