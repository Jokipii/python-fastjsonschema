"""Module for format handling."""

import re
import jsonpointer
import email_validator
from email_validator import validate_email
from email_validator import validate_email_domain_part
import rfc3987
from expynent.patterns import (
    ISO_8601_DATETIME,
    EMAIL_ADDRESS,
    IP_V4,
    IP_V6
)


DATE_REGEX = re.compile(
    r'^(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})$'
)

DATETIME_REGEX = re.compile(ISO_8601_DATETIME, re.IGNORECASE)

EMAIL_REGEX = re.compile(EMAIL_ADDRESS)

HOSTNAME_REGEX = re.compile(
    r'^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*'
    r'([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]{1,62}[A-Za-z0-9])$'
)

IPV4_REGEX = re.compile(IP_V4)

IPV6_REGEX = re.compile(IP_V6, re.VERBOSE | re.IGNORECASE | re.DOTALL)

RELATIVE_JSON_POINTER_REGEX = re.compile(r'^(?:0|[1-9][0-9]*)(?:#|(?:\/(?:[^~/]|~0|~1)*)*)$')

TIME_REGEX = re.compile(
    r'^(?P<hour>\d{1,2}):(?P<minute>\d{1,2})'
    r'(?::(?P<second>\d{1,2})(?:\.(?P<microsecond>\d{1,6}))?([zZ]|[+-]\d\d:\d\d)?)?$'
)

URI_REGEX = re.compile(r'^\w+:(\/?\/?)[^\s]+$')

URI_TEMPLATE_REGEX = re.compile(
    r'^(?:(?:[^\x00-\x20\"\'<>%\\^`{|}]|%[0-9a-f]{2})|'
    r'\{[+#./;?&=,!@|]?(?:[a-z0-9_]|%[0-9a-f]{2})+'
    r'(?::[1-9][0-9]{0,3}|\*)?(?:,(?:[a-z0-9_]|%[0-9a-f]{2})+'
    r'(?::[1-9][0-9]{0,3}|\*)?)*\})*$',
    re.IGNORECASE
)

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
    try:
        return validate_email(
            email=variable,
            allow_smtputf8=True,
            check_deliverability=False
        )
    except email_validator.EmailSyntaxError:
        return False


def is_valid_idn_hostname(variable):
    """
    Validate idn-hostnames.

    :argument str variable: variable to validate.
    :rtype: bool: False if invalid.
    """
    try:
        return validate_email_domain_part(variable)
    except email_validator.EmailSyntaxError:
        return False


def is_valid_iri(variable):
    """
    Validate iRIs.

    :argument str variable: variable to validate.
    :rtype: bool: False if invalid.
    """
    try:
        return rfc3987.parse(variable, rule="IRI")
    except ValueError:
        return False


def is_valid_iri_reference(variable):
    """
    Validate IRI-references.

    :argument str variable: variable to validate.
    :rtype: bool: False if invalid.
    """
    try:
        return rfc3987.parse(variable, rule="IRI_reference")
    except ValueError:
        return False


def is_valid_json_pointer(variable):
    """
    Validate json-ponsters.

    :argument str variable: variable to validate.
    :rtype: bool: False if invalid.
    """
    try:
        return jsonpointer.JsonPointer(pointer=variable)
    except jsonpointer.JsonPointerException:
        return False


def is_valid_regexp(variable):
    """
    Validate regexp.

    :argument str variable: variable to validate.
    :rtype: bool: False if invalid.
    """
    try:
        re.compile(pattern=variable)
        return True
    except re.error:
        return False


def is_valid_uri_reference(variable):
    """
    Validate URI-references.

    :argument str variable: variable to validate.
    :rtype: bool: False if invalid.
    """
    try:
        return rfc3987.parse(variable, rule="URI_reference")
    except ValueError:
        return False


FORMAT_FUNCTIONS = {
    'idn-email': 'is_valid_idn_email',
    'idn-hostname': 'is_valid_idn_hostname',
    'iri': 'is_valid_iri',
    'iri-reference': 'is_valid_iri_reference',
    'json-pointer': 'is_valid_json_pointer',
    'regex': 'is_valid_regexp',
    'uri-reference': 'is_valid_uri_reference',
}
