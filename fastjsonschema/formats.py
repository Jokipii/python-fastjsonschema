"""Module for format handling."""

import re
from collections import namedtuple

from expynent import patterns

from fastjsonschema.exceptions import JsonSchemaException


RegExConfig = namedtuple('RegExConfig', ['pattern', 'flags'])


DATE_REGEX = RegExConfig(
    r'^(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})$', 0)
DATETIME_REGEX = RegExConfig(patterns.ISO_8601_DATETIME, re.IGNORECASE)
EMAIL_REGEX = RegExConfig(patterns.EMAIL_ADDRESS, 0)
HOSTNAME_REGEX = RegExConfig(
    r'^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*'
    r'([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]{1,62}[A-Za-z0-9])$', 0)
IPV4_REGEX = RegExConfig(patterns.IP_V4, 0)
IPV6_REGEX = RegExConfig(
    patterns.IP_V6, re.VERBOSE | re.IGNORECASE | re.DOTALL)
RELATIVE_JSON_POINTER_REGEX = RegExConfig(
    r'^(?:0|[1-9][0-9]*)(?:#|(?:\/(?:[^~/]|~0|~1)*)*)$', 0)
TIME_REGEX = RegExConfig(
    r'^(?P<hour>\d{1,2}):(?P<minute>\d{1,2})'
    r'(?::(?P<second>\d{1,2})(?:\.(?P<microsecond>\d{1,6}))?'
    r'([zZ]|[+-]\d\d:\d\d)?)?$', 0)
URI_REGEX = RegExConfig(r'^\w+:(\/?\/?)[^\s]+$', 0)
URI_TEMPLATE_REGEX = RegExConfig(
    r'^(?:(?:[^\x00-\x20\"\'<>%\\^`{|}]|%[0-9a-f]{2})|'
    r'\{[+#./;?&=,!@|]?(?:[a-z0-9_]|%[0-9a-f]{2})+'
    r'(?::[1-9][0-9]{0,3}|\*)?(?:,(?:[a-z0-9_]|%[0-9a-f]{2})+'
    r'(?::[1-9][0-9]{0,3}|\*)?)*\})*$', re.IGNORECASE)


FORMAT_REGEXS = {
    'date': DATE_REGEX,
    'date-time': DATETIME_REGEX,
    'email': EMAIL_REGEX,
    'hostname': HOSTNAME_REGEX,
    'ipv4': IPV4_REGEX,
    'ipv6': IPV6_REGEX,
    'relative-json-pointer': RELATIVE_JSON_POINTER_REGEX,
    'time': TIME_REGEX,
    'uri': URI_REGEX,
    'uri-template': URI_TEMPLATE_REGEX,
}


def is_valid_idn_email(variable):
    """
    Validate idn-emails.

    :argument str variable: variable to validate.
    :rtype: bool: False if invalid.
    """
    import email_validator
    try:
        return email_validator.validate_email(
            email=variable,
            allow_smtputf8=True,
            check_deliverability=False
        )
    except email_validator.EmailSyntaxError:
        return False
    return True


def is_valid_idn_hostname(variable):
    """
    Validate idn-hostnames.

    :argument str variable: variable to validate.
    :rtype: bool: False if invalid.
    """
    import email_validator
    try:
        return email_validator.validate_email_domain_part(variable)
    except email_validator.EmailSyntaxError:
        return False
    return True


def is_valid_iri(variable):
    """
    Validate iRIs.

    :argument str variable: variable to validate.
    :rtype: bool: False if invalid.
    """
    try:
        import rfc3987
        return rfc3987.parse(variable, rule="IRI")
    except ValueError:
        return False
    return True


def is_valid_iri_reference(variable):
    """
    Validate IRI-references.

    :argument str variable: variable to validate.
    :rtype: bool: False if invalid.
    """
    try:
        import rfc3987
        return rfc3987.parse(variable, rule="IRI_reference")
    except ValueError:
        return False
    return True


def is_valid_json_pointer(variable):
    """
    Validate json-ponsters.

    :argument str variable: variable to validate.
    :rtype: bool: False if invalid.
    """
    import jsonpointer
    try:
        jsonpointer.JsonPointer(pointer=variable)
    except jsonpointer.JsonPointerException:
        return False
    return True


def is_valid_regexp(variable):
    """
    Validate regexp.

    :argument str variable: variable to validate.
    :rtype: bool: False if invalid.
    """
    try:
        re.compile(pattern=variable)
    except re.error:
        return False
    return True


def is_valid_uri_reference(variable):
    """
    Validate URI-references.

    :argument str variable: variable to validate.
    :rtype: bool: False if invalid.
    """
    try:
        import rfc3987
        return rfc3987.parse(variable, rule="URI_reference")
    except ValueError:
        return False


FORMAT_FUNCTIONS = {
    'idn-email': is_valid_idn_email,
    'idn-hostname': is_valid_idn_hostname,
    'iri': is_valid_iri,
    'iri-reference': is_valid_iri_reference,
    'json-pointer': is_valid_json_pointer,
    'regex': is_valid_regexp,
    'uri-reference': is_valid_uri_reference,
}


class FormatResolver(object):
    """
    Class to handle all differet formats

    :param dict functions: Dicti of validations functions.
    :param dict regexs: Dict of regex partters and compilation
        parameters
    """

    def __init__(self, functions: dict = None, regexs: dict = None):
        """Init."""
        format_functions = FORMAT_FUNCTIONS
        format_regexs = FORMAT_REGEXS
        self._functions = format_functions if functions is None else format_functions.update(functions)
        self._regexs = format_regexs if regexs is None else format_regexs.update(regexs)
        self._regex_cache = {}

    def has(self, name):
        """Resturn True if name exists"""
        return (
            name in self._functions
            or name in self._regex_cache
            or name in self._regexs
        )

    def get_function(self, name):
        """Resturn a validation function"""
        if name in self._functions:
            return self._functions[name]
        if not name in self._regex_cache:
            self._compile_regex(name)
        return self._regex_cache[name]

    def get_function_name(self, name):
        """Resturns name of function"""
        if not name in self._functions:
            raise JsonSchemaException('Format function not found: ' + name)
        func = self._functions[name]
        return func.__name__

    def _compile_regex(self, name):
        value = re.compile(*self._regexs[name])
        self._regex_cache[name] = value
        return
