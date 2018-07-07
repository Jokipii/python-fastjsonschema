import re

from fastjsonschema.utils import *


def test_split_words():
    cases = [
        ([""], ""),
        ([""], "   "),
        (["x"], " x "),
        (["foo", "bar"], "foo bar"),
        (["foo", "bar"], "foo\n\tbar"),
        (["foo", "bar"], "foo\r\nbar"),
        (["foo", "bar"], "foo-bar"),
        (["foo", "Bar"], "fooBar"),
        (["Foo", "Bar"], "FooBar"),
        (["foo", "bar"], "foo_bar"),
        (["FOO", "BAR"], "FOO_BAR"),
        (["IP", "Address"], "IPAddress"),
        (["Adler", "32"], "Adler32"),
        (["Inet", "4", "Address"], "Inet4Address"),
        (["Arc", "2", "D"], "Arc2D"),
        (["a", "123b"], "a123b"),
        (["A", "123", "B"], "A123B"),
    ]
    for x, y in cases:
        assert x == split_words(y)


def test_get_valid_class_name():
    cases = [
        ("UserAgent", "user-agent"),
        ("Dnt", "dnt"),
        ("RemoteIp", "remote-ip"),
        ("Re", "re"),
        ("UaCpu", "ua-cpu"),
        ("XSslCipher", "x-ssl-cipher"),
        ("XWapProfile", "x-wap-profile"),
        ("XXssProtection", "x-xss-protection"),
        ("HttpJsonSchemaOrgDraft07Schema", "http://json-schema.org/draft-07/schema#")
    ]
    for x, y in cases:
        assert x == get_valid_class_name(y)


def test_get_valid_function_name():
    cases = [
        ("user_agent", "user-agent"),
        ("dnt", "dnt"),
        ("remote_ip", "remote-ip"),
        ("re", "re"),
        ("ua_cpu", "ua-cpu"),
        ("x_ssl_cipher", "x-ssl-cipher"),
        ("x_wap_profile", "x-wap-profile"),
        ("x_xss_protection", "x-xss-protection"),
        ("http_json_schema_org_draft07_schema", "http://json-schema.org/draft-07/schema#")
    ]
    for x, y in cases:
        assert x == get_valid_function_name(y)
