"""Main module."""

import json
import sys

import click

from . import compile_to_code
from .version import VERSION


@click.command()
@click.option(
    '-s',
    '--schema-file',
    type=click.STRING,
    help="Schema file name",
)
@click.option(
    '-o',
    '--output-file',
    type=click.STRING,
    help="Output file name"
)
@click.argument(
    'schema',
    type=click.STRING,
    default='-',
)
@click.argument(
    'output',
    type=click.STRING,
    default='-',
)
def main(schema, output, output_file, schema_file):
    """
    Ccommand-line usage examples:

    echo '{"type": "string"}' | fastjsonschema > your_file.py
    
    fastjsonschema '{"type": "string"}' > your_file.py

    """

    if not output is '-':
        click.secho('Fast JSON schema validator - version {}'.format(VERSION), fg='green')

    if schema_file:
        with click.open_file(schema_file, mode='r', encoding='utf-8') as fp:
            definition = fp.read()
    elif schema == '-':
        with click.open_file(schema, mode='r', encoding='utf-8') as fp:
            definition = fp.read()
    else:
        definition = schema

    definition = json.loads(definition)
    name, code = compile_to_code(definition)

    if output_file:
        with click.open_file(output_file, mode='w', encoding='utf-8') as fp:
            click.echo(code, file=fp)
        if not output is '-':
            click.echo(''.join([
                'Schema written in: ',
                click.style('{}'.format(output), fg='green'),
                ', main function is: ',
                click.style('{}'.format(name), fg='blue'),
            ]))
    else:
        click.echo(code)


if __name__ == '__main__':
    main()
