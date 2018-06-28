import re
import jsonpointer
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
    r'(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})$'
)

TIME_REGEX = re.compile(
    r'(?P<hour>\d{1,2}):(?P<minute>\d{1,2})'
    r'(?::(?P<second>\d{1,2})(?:\.(?P<microsecond>\d{1,6})\d{0,6})?)?'
)

DATETIME_REGEX = re.compile(ISO_8601_DATETIME)

EMAIL_REGEX = re.compile(EMAIL_ADDRESS)

IPV4_REGEX = re.compile(IP_V4)

IPV6_REGEX = re.compile(IP_V6, re.VERBOSE | re.IGNORECASE | re.DOTALL)

HOSTNAME_REGEX = re.compile(
    r'^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*'
    r'([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]{1,62}[A-Za-z0-9])$'
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
    'time': TIME_REGEX,
    'uri': URI_REGEX,
    'uri-template': URI_TEMPLATE_REGEX,
}


def check_idn_email(variable):
    return validate_email(
        variable,
        allow_smtputf8=True,
        check_deliverability=False
    )


def check_idn_hostname(variable):
    return validate_email_domain_part(variable)


def check_iri(variable):
    return rfc3987.parse(variable, rule="IRI")


def check_iri_reference(variable):
    return rfc3987.parse(variable, rule="IRI_reference")


def check_json_pointer(variable):
    return jsonpointer.JsonPointer(variable)


def check_regexp(variable):
    try:
        re.compile(variable)
        return True
    except re.error:
        return False


FORMAT_FUNCTIONS = {
    'idn-email': 'check_idn_email',
    'idn-hostname': 'check_idn_hostname',
    'iri': 'check_iri',
    'iri-reference': 'check_iri_reference',
    'json-pointer': 'check_json_pointer',
    'regex': 'check_regexp',
}
