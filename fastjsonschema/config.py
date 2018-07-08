"""Config module"""


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
    :argument bool ecma262_regex_non_compliance: wheter check
        and disallow non compliant versions of regexps
    :returns: the Configuration.
    """

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            schema_version="draft7",
            uri_handlers: dict = None,
            cache_refs=True,
            validate_schema=False,
            include_version=False,
            ecma262_regex_non_compliance=True,
    ):
        """Init."""
        self.schema_version = schema_version
        self.uri_handlers = uri_handlers if uri_handlers else {}
        self.cache_refs = cache_refs
        self.validate_schema = validate_schema
        self.include_version = include_version
        self.ecma262_regex_non_compliance = ecma262_regex_non_compliance
