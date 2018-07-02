"""
This project was made to come up with fast JSON validations. Just let's see some numbers first:

 * Probalby most popular ``jsonschema`` can take in tests up to 5 seconds for valid inputs
   and 1.2 seconds for invalid inputs.
 * Secondly most popular ``json-spec`` is even worse with up to 7.2 and 1.7 seconds.
 * Lastly ``validictory`` is much better with 370 or 23 miliseconds, but it does not
   follow all standards and it can be still slow for some purposes.

That's why this project exists. It compiles definition into Python most stupid code
which people would had hard time to write by themselfs because of not-written-rule DRY
(don't repeat yourself). When you compile definition, then times are 25 miliseconds for
valid inputs and less than 2 miliseconds for invalid inputs. Pretty amazing, right? :-)

You can try it for yourself with included script:

.. code-block:: bash

    $ make performance
    fast_compiled        valid      ==> 0.026877017982769758
    fast_compiled        invalid    ==> 0.0015628149849362671
    fast_file            valid      ==> 0.025493122986517847
    fast_file            invalid    ==> 0.0012430319911800325
    fast_not_compiled    valid      ==> 4.790547857992351
    fast_not_compiled    invalid    ==> 1.2642899919883348
    jsonschema           valid      ==> 5.036152001994196
    jsonschema           invalid    ==> 1.1929481109953485
    jsonspec             valid      ==> 7.196442283981014
    jsonspec             invalid    ==> 1.7245555499684997
    validictory          valid      ==> 0.36818933801259845
    validictory          invalid    ==> 0.022672351042274386

This library follows and implements `JSON schema draft-04, draft-06,
amd draft-07 <http://json-schema.org>`_. Sometimes it's not perfectly clear
so I recommend also check out this `understaning json schema
<https://spacetelescope.github.io/understanding-json-schema>`_.

Note that there are some differences compared to JSON schema standard:

 * Regular expressions are full Python ones, not only what JSON schema allows.
   It's easier to allow everything and also it's faster to compile without
   limits. So keep in mind that when you will use more advanced regular
   expression, it may not work with other library.
 * JSON schema says you can use keyword ``default`` for providing default
   values. This implementation uses that and always returns transformed
   input data.

Support only for Python 3.3 and higher.
"""

from os.path import exists

from .exceptions import JsonSchemaException
from .generator import CodeGenerator
from .ref_resolver import RefResolver
from .version import VERSION

__all__ = ('VERSION', 'JsonSchemaException', 'compile', 'compile_to_code')


# pylint: disable=redefined-builtin,exec-used
def compile(definition, handlers=None, schema_version='draft4'):
    """
    Generates validation function for validating JSON schema by ``definition``.

    :argument dict definition: Json schema definition
    :argument dict handlers: A mapping from URI schemes to functions
        that should be used to retrieve them.
    :argument str schema_version: Meta schema version where definition
        is created.
    :returns: the validator instance specified by schema definition

    Exception :any:`JsonSchemaException` is thrown when validation fails.

    Example:

    .. code-block:: python

        import fastjsonschema

        validate = fastjsonschema.compile({'type': 'string'})
        validate('hello')

    This implementation support keyword ``default``:

    .. code-block:: python

        validate = fastjsonschema.compile({
            'type': 'object',
            'properties': {
                'a': {'type': 'number', 'default': 42},
            },
        })

        data = validate({})
        assert data == {'a': 42}

    """
    resolver, code_generator = _factory(definition, schema_version, handlers)
    global_state = code_generator.global_state
    # Do not pass local state so it can recursively call itself.
    exec(code_generator.func_code, global_state)
    _, name = resolver.get_scope_name()
    return global_state[name]


def compile_to_code(definition, handlers=None, schema_version='draft4'):
    """
    Generates validation function for validating JSON schema by ``definition``
    and returns compiled code.

    :argument dict definition: Json schema definition
    :argument dict handlers: A mapping from URI schemes to functions
        that should be used to retrieve them.
    :argument str schema_version: Meta schema version where definition
        is created.
    :returns: tuple(str, str): function name, actual code

    Exception :any:`JsonSchemaException` is thrown when validation fails.

    Example:

    .. code-block:: python

        import fastjsonschema

        code = fastjsonschema.compile_to_code({'type': 'string'})
        with open('your_file.py', 'w') as f:
            f.write(code)

    You can also use it as a script:

    .. code-block:: bash

        echo '{"type": "string"}' | python3 -m fastjsonschema > your_file.py
        python3 -m fastjsonschema '{"type": "string"}' > your_file.py

    """
    resolver, code_generator = _factory(definition, schema_version, handlers)
    _, name = resolver.get_scope_name()
    return name, (
        code_generator.global_state_code + '\n' +
        'VERSION = "' + VERSION + '"\n' +
        code_generator.func_code
    )


def _factory(schema, schema_version='draft4', handlers=None):
    resolver = RefResolver.from_schema(
        schema=schema,
        schema_version=schema_version,
        handlers=handlers
    )
    code_generator = CodeGenerator(resolver=resolver)
    return resolver, code_generator
