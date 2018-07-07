"""
This project was made to come up with fast JSON validations.

Just let's see some numbers first:

 * Probalby most popular ``jsonschema`` can take in tests up to 5 seconds
   for valid inputs and 1.2 seconds for invalid inputs.
 * Secondly most popular ``json-spec`` is even worse with up to 7.2 and
   1.7 seconds.
 * Lastly ``validictory`` is much better with 370 or 23 miliseconds, but it
   does not follow all standards and it can be still slow for some purposes.

That's why this project exists. It compiles definition into Python most
stupid code which people would had hard time to write by themselfs because
of not-written-rule DRY (don't repeat yourself). When you compile definition,
then times are 25 miliseconds for valid inputs and less than 2 miliseconds
for invalid inputs. Pretty amazing, right? :-)

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

Support only for Python 3.4 and higher.
"""

__all__ = (
    '__version__',
    'Config',
    'JsonSchemaException',
    'compile',
    'compile_to_code',
)

from os.path import exists
import json
import importlib

import click

from .exceptions import JsonSchemaException
from .generator import CodeGenerator
from .ref_resolver import RefResolver
from .formats import FormatResolver
from .version import __version__


# pylint: disable=too-few-public-methods
class Config(object):
    """
    Configuration options.

    :argument str schema_version: Meta schema version where definition
        is created. This is used if schema itsef doesn't have
        valid refeerence ``$scheme``. Default is ```draft7``.
    :argument dict handlers: A mapping from ``URI schemes`` as ``str``
        to functions that should be used to retrieve schema parts.
        Function must ta ke ``uri`` as argument and return valid schema
        as ``dict`` or throw ``JsonSchemaException``.
    :argument bool cache_refs: whether remote refs should be cached after
        first resolution. Default True.
    :argument bool validate_schema: whether schema should be validated
        against it meta schema. Default False.
    :argument bool include_version: whether library version is included
        in generated code. Default False.
    :returns: the Configuration.
    """

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            schema_version: str = "draft7",
            uri_handlers: dict = None,
            cache_refs: bool = True,
            validate_schema: bool = False,
            include_version: bool = False,
    ):
        """Init."""
        self.schema_version = schema_version
        self.uri_handlers = uri_handlers if uri_handlers else {}
        self.cache_refs = cache_refs
        self.validate_schema = validate_schema
        self.include_version = include_version


# pylint: disable=redefined-builtin,exec-used
def compile(definition, config=None):
    """
    Generate validation function for validating JSON schema by ``definition``.

    :argument dict definition: Json schema definition
    :argument Config config: Config object
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
    name, code_generator = _factory(definition, config)
    global_state = code_generator.global_state
    # Do not pass local state so it can recursively call itself.
    exec(code_generator.code, global_state)
    return global_state[name]


def compile_to_code(definition, config=None):
    """
    Generate validation function as plain Python code.

    :argument dict definition: Json schema definition
    :argument Config config: Config object
    :returns: tuple(str, str): main validation function name, actual code

    Exception :any:`JsonSchemaException` is thrown when validation fails.

    Example:

    .. code-block:: python

        import fastjsonschema

        code = fastjsonschema.compile_to_code({'type': 'string'})
        with open('your_file.py', 'w') as f:
            f.write(code)

    You can also use it as a script:

    .. code-block:: bash

        echo '{"type": "string"}' | fastjsonschema > your_file.py
        fastjsonschema '{"type": "string"}' > your_file.py

    """
    name, code_generator = _factory(definition, config)
    return name, code_generator.code


def _factory(schema, config=None):
    config = config if config else Config()
    resolver = RefResolver.from_schema(schema=schema, config=config)
    if config.validate_schema:
        from copy import deepcopy
        data = deepcopy(resolver.schema)
        resolver.meta_schema.validate(data)
    format_resolver = FormatResolver()
    code_generator = CodeGenerator(resolver=resolver, formats=format_resolver)
    _, name = resolver.get_scope_name()
    return name, code_generator


@click.command()
@click.option(
    '-s',
    '--schema-file',
    type=click.STRING,
    help="Schema file name",
    default=None,
)
@click.option(
    '-o',
    '--output-file',
    type=click.STRING,
    help="Output file name",
    default=None,
)
@click.option(
    '-p',
    '--python-schema',
    type=click.STRING,
    help="Python module and function name",
    default=None,
)
@click.option(
    '-v',
    '--validate-file',
    type=click.STRING,
    help="Validate file name",
    default=None,
)
@click.argument(
    'schema',
    type=click.STRING,
    default='-'
)
@click.argument(
    'output',
    type=click.STRING,
    default='-',
)
# pylint: disable=too-many-arguments
def main(
        schema='-',
        output='-',
        output_file=None,
        schema_file=None,
        validate_file=None,
        python_schema=None,
):
    """
    Ccommand line usage examples


    Create validation function and store it as python file:

    echo '{"type": "string"}' | fastjsonschema > your_file.py

    fastjsonschema '{"type": "string"}' > your_file.py


    Validate document:

    fastjsonschema -s openapi-3.0.json -v api-example.json

    fastjsonschema -p "exampke schema" -v example.json

    """
    validator = None

    if output != '-' or validate_file:
        click.secho(
            'Fast JSON schema validator - version {}'.format(__version__),
            fg='green'
        )

    if schema_file:
        with click.open_file(
            schema_file, mode='r', encoding='utf-8'
        ) as file_handle:
            definition = file_handle.read()
    elif schema == '-':
        with click.open_file(
            schema, mode='r', encoding='utf-8'
        ) as file_handle:
            definition = file_handle.read()
    elif python_schema:
        click.echo('here')
        module, validator = python_schema.split(' ')
        validator = importlib.import_module(module, validator)
    else:
        definition = schema

    definition = json.loads(definition)
    if not validate_file:
        name, code = compile_to_code(definition)
    else:
        if not validator:
            validator = compile(definition)
        with open(validate_file, encoding='utf-8') as file_handle:
            data = file_handle.read()
        try:
            validator(json.loads(data))
            click.secho('Document is valid', fg='green')
            return True
        except JsonSchemaException as exception:
            click.echo(exception.message)
            click.secho('Document is invalid', fg='red')
            return False

    if output_file:
        with click.open_file(
            output_file, mode='w', encoding='utf-8'
        ) as file_handle:
            click.echo(code, file=file_handle)
        if output != '-':
            click.echo(''.join([
                'Schema written in: ',
                click.style('{}'.format(output), fg='green'),
                ', main function is: ',
                click.style('{}'.format(name), fg='blue'),
            ]))
    else:
        click.echo(code)
    return True


if __name__ == '__main__':
    main()
