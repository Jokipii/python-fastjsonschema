"""Main module."""

import json
import importlib

import click

# pylint: disable=redefined-builtin
from . import compile, compile_to_code, JsonSchemaException
from .version import __version__


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
def main(schema, output, output_file, schema_file, validate_file, python_schema):
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
        click.secho('Fast JSON schema validator - version {}'.format(__version__), fg='green')

    if schema_file:
        with click.open_file(schema_file, mode='r', encoding='utf-8') as file_handle:
            definition = file_handle.read()
    elif schema == '-':
        with click.open_file(schema, mode='r', encoding='utf-8') as file_handle:
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
        with click.open_file(output_file, mode='w', encoding='utf-8') as file_handle:
            click.echo(code, file=file_handle)
        if not output == '-':
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
    pass
