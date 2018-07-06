"""
Module for JSON reference resolving.

Specification: JSON Schema URI resolution scopes and dereferencing.
https://tools.ietf.org/id/draft-zyp-json-schema-04.html#rfc.section.7

Code adapted from https://github.com/Julian/jsonschema
"""
import contextlib
import re
from urllib import parse as urlparse
from urllib.parse import unquote
from urllib.request import urlopen
import json

import requests

from fastjsonschema.meta_schema import MetaSchema
from fastjsonschema.exceptions import JsonSchemaException


def resolve_path(schema: dict, fragment: str):
    """
    Return definition from path.

    Path is unescaped according https://tools.ietf.org/html/rfc6901

    :argument schema: the referrant schema document
    :argument str fragment: a URI fragment to resolve within it
    :returns: the retrieved schema definition

    """
    fragment = fragment.lstrip('/')
    parts = unquote(fragment).split('/') if fragment else []
    for part in parts:
        part = part.replace('~1', '/').replace('~0', '~')
        if isinstance(schema, list):
            schema = schema[int(part)]
        elif part in schema:
            schema = schema[part]
        else:
            raise JsonSchemaException('Unresolvable ref: {}'.format(part))
    return schema


def normalize(uri: str):
    """
    Normalize URI's.

    :argument str uri: the URI to be normalized
    :returns: normalized version of URI
    """
    return urlparse.urlsplit(uri).geturl()


def resolve_remote(uri: str, handlers: dict):
    """
    Resolve a remote ``uri``.

    .. note::

        Requests_ library is used to fetch ``http`` or ``https``
        requests from the remote ``uri``, if handlers does not
        define otherwise.

        For unknown schemes urlib is used with UTF-8 encoding.

    .. _Requests: http://pypi.python.org/pypi/requests/

    :argument str uri: the URI to resolve
    :argument dict handlers: the URI resolver functions for each scheme
    :returns: the retrieved schema document

    """
    scheme = urlparse.urlsplit(uri).scheme
    if scheme in handlers:
        result = handlers[scheme](uri)
    elif scheme in ['http', 'https']:
        result = requests.get(uri).json()
    else:
        result = json.loads(urlopen(uri).read().decode('utf-8'))
    return result


class RefResolver(object):
    """Class to resolve JSON References."""

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            base_uri: str,
            schema: dict,
            meta_schema: str,
            config,
    ):
        """
        Construct a resolver from a JSON schema object.

        :argument str base_uri: URI of the referring document
        :argument dict schema: the referring schema
        :argument str meta_schema: schema's meta schema
        :argument Config config: config object
        :rtype: :class:`RefResolver`

        """
        self.base_uri = base_uri
        self.resolution_scope = base_uri
        self.schema = schema
        self.meta_schema = meta_schema
        self.config = config
        self.uri_cache = {}
        self.walk(schema)
        if self.config.validate_schema:
            meta_schema.validator(schema)

    @classmethod
    def from_schema(cls, schema, config):
        """
        Static helper to construct a resolver from a JSON schema object.

        :argument dict schema: the referring schema
        :argument Config config: config object
        :rtype: :class:`RefResolver`

        If schema_version is defined in actual schema it is used instead of
        config.meta_schema.
        """
        if isinstance(schema, dict) and '$schema' in schema:
            schema_version = schema['$schema']
        else:
            schema_version = config.schema_version
        meta_schema = MetaSchema(schema_version)
        id_type = meta_schema.id_type
        return cls(
            schema.get(id_type, '') if isinstance(schema, dict) else '',
            schema,
            meta_schema=meta_schema,
            config=config
        )

    @contextlib.contextmanager
    def in_scope(self, scope: str):
        """
        Context manager to handle cprrent scope.

        :argument str scope: new scope
        """
        old_scope = self.resolution_scope
        self.resolution_scope = urlparse.urljoin(old_scope, scope)
        try:
            yield
        finally:
            self.resolution_scope = old_scope

    @contextlib.contextmanager
    def resolving(self, ref: str):
        """
        Context manager which resolves a JSON ``ref``.

        :argument str ref: reference to resolve
        """
        new_uri = urlparse.urljoin(self.resolution_scope, ref)
        uri, fragment = urlparse.urldefrag(new_uri)

        if normalize(uri) in self.uri_cache:
            schema = self.uri_cache[normalize(uri)]
        elif not uri or uri == self.base_uri:
            schema = self.schema
        else:
            schema = resolve_remote(uri, self.config.uri_handlers)
            if self.config.cache_refs:
                self.uri_cache[normalize(uri)] = schema

        old_base_uri, old_schema = self.base_uri, self.schema
        self.base_uri, self.schema = uri, schema
        try:
            with self.in_scope(uri):
                yield resolve_path(schema, fragment)
        finally:
            self.base_uri, self.schema = old_base_uri, old_schema

    def get_scope_name(self, postfix: str = ''):
        """
        Get current scope and return it as a valid function name.

        :argument str postfix: Possible postfix for name
        :rtyper: :(str, str): Uri, Function name based on current scope.
        """
        name = 'validate_' + unquote(
            self.resolution_scope).replace('~1', '_').replace('~0', '_')
        name = re.sub(r'[:/#\.\-\%]+', '_', name) + postfix
        name = name.lower().rstrip('_')
        return normalize(self.resolution_scope), name

    def walk(self, node: dict):
        """
        Walk thru schema and dereferencing ``id`` and ``$ref`` instances.

        :argument dict node: Schema node.
        """
        _id = self.meta_schema.id_type
        if isinstance(node, bool):
            pass
        elif '$ref' in node and isinstance(node['$ref'], str):
            ref = node['$ref']
            node['$ref'] = urlparse.urljoin(self.resolution_scope, ref)
        elif _id in node and isinstance(node[_id], str):
            with self.in_scope(node[_id]):
                self.uri_cache[normalize(self.resolution_scope)] = node
                for _, item in node.items():
                    if isinstance(item, dict):
                        self.walk(item)
        else:
            for _, item in node.items():
                if isinstance(item, dict):
                    self.walk(item)
