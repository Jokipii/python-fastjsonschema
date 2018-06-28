"""
JSON Schema URI resolution scopes and dereferencing

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

from .meta_schema import MetaSchema
from .exceptions import JsonSchemaException
from .meta_schema import meta_schemas


def resolve_path(schema, fragment):
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


def normalize(uri):
    return urlparse.urlsplit(uri).geturl()


def resolve_remote(uri, handlers):
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
    """
    Resolve JSON References.

    :argument str base_uri: URI of the referring document
    :argument schema: the actual referring schema document
    :argument dict store: a mapping from URIs to documents to cache
    :argument bool cache: whether remote refs should be cached after
        first resolution
    :argument dict handlers: a mapping from URI schemes to functions that
        should be used to retrieve them

    """

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            base_uri,
            schema,
            meta_schema,
            store=None,
            cache=True,
            handlers=None
    ):
        self.base_uri = base_uri
        self.resolution_scope = base_uri
        self.schema = schema
        self.meta_schema = meta_schema
        if store is None:
            store = {}
        self.store = store
        self.cache = cache
        if handlers is None:
            handlers = {}
        self.handlers = handlers
        self.walk(schema)

        # meta-schemas: draft-04, draft-06, draft-07
        for uri, schema in meta_schemas.items():
            self.store[uri] = schema


    @classmethod
    def from_schema(cls, schema, schema_version='draft4', handlers=None, **kwargs):
        """
        Construct a resolver from a JSON schema object.

        :argument dict schema: the referring schema
        :argument str schema_version: Meta schema version of the referring schema
        :argument dict handlers: A mapping from URI schemes to functions
            that should be used to retrieve them.
        :rtyper: :class:`RefResolver`

        """
        # if schema_version is defined in schema we use it
        if '$schema' in schema:
            schema_version = schema['$schema']
        meta_schema = MetaSchema(schema_version)
        return cls(
            schema.get(meta_schema.id_type, ''),
            schema,
            meta_schema=meta_schema,
            handlers=handlers,
            **kwargs
        )

    @contextlib.contextmanager
    def in_scope(self, scope):
        old_scope = self.resolution_scope
        self.resolution_scope = urlparse.urljoin(old_scope, scope)
        try:
            yield
        finally:
            self.resolution_scope = old_scope

    @contextlib.contextmanager
    def resolving(self, ref):
        """
        Context manager which resolves a JSON ``ref`` and enters the
        resolution scope of this ref.

        :argument str ref: reference to resolve

        """
        new_uri = urlparse.urljoin(self.resolution_scope, ref)
        uri, fragment = urlparse.urldefrag(new_uri)

        if normalize(uri) in self.store:
            schema = self.store[normalize(uri)]
        elif not uri or uri == self.base_uri:
            schema = self.schema
        else:
            schema = resolve_remote(uri, self.handlers)
            if self.cache:
                self.store[normalize(uri)] = schema

        old_base_uri, old_schema = self.base_uri, self.schema
        self.base_uri, self.schema = uri, schema
        try:
            with self.in_scope(uri):
                yield resolve_path(schema, fragment)
        finally:
            self.base_uri, self.schema = old_base_uri, old_schema

    def get_uri(self):
        return normalize(self.resolution_scope)

    def get_scope_name(self):
        name = 'validate_' + unquote(self.resolution_scope).replace('~1', '_').replace('~0', '_')
        name = re.sub(r'[:/#\.\-\%]', '_', name)
        name = name.lower().rstrip('_')
        return name

    def walk(self, node: dict):
        """
        Walk thru schema and dereferencing ``id`` and ``$ref`` instances
        """
        _id = self.meta_schema.id_type
        if '$ref' in node and isinstance(node['$ref'], str):
            ref = node['$ref']
            node['$ref'] = urlparse.urljoin(self.resolution_scope, ref)
        elif _id in node and isinstance(node[_id], str):
            with self.in_scope(node[_id]):
                self.store[normalize(self.resolution_scope)] = node
                for _, item in node.items():
                    if isinstance(item, dict):
                        self.walk(item)
        else:
            for _, item in node.items():
                if isinstance(item, dict):
                    self.walk(item)
