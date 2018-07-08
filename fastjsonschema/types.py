"""Types module."""

from copy import deepcopy

def enforce_list(value):
    """Change anything to list."""
    if isinstance(value, list):
        return value
    return [value]


JSON_TYPE_TO_PYTHON_TYPE = {
    'object': 'dict',
    'string': 'str',
    'number': 'int, float',
    'integer': 'int',
    'boolean': 'bool',
    'null': 'NoneType',
    'array': 'list',
}


class TypeResolver(object):
    """JsonTypeResolver."""

    def __init__(self, version):
        """Init."""
        self.json_to_python = deepcopy(JSON_TYPE_TO_PYTHON_TYPE)
        if version == "http://json-schema.org/draft-04/schema#":
            self._float_integer = None
        else:
            self._float_integer = " and not (isinstance({variable}, float) and {variable}.is_integer())"

    def type_definition_list(self, values):
        types = enforce_list(values)
        python_types = ', '.join(self.json_to_python[t] for t in types)
        extra = ''
        if 'integer' in types and self._float_integer:
            # for zeroTerminatedFloats.json in draft-06 and in draft-07
            # some languages do not distinguish between different types of numeric value
            # a float without fractional part is an integer
            extra += self._float_integer
        if ('number' in types or 'integer' in types) and 'boolean' not in types:
            extra += ' or isinstance({variable}, bool)'
        if_statement = 'if not isinstance({{variable}}, ({})){}:'.format(python_types, extra)
        raise_statement = 'raise JsonSchemaException("{{name}} must be {}")'.format(' or '.join(types))
        return if_statement, raise_statement
