# pylint: skip-file
import re
from fastjsonschema.formats import is_valid_uri_reference
from fastjsonschema.formats import is_valid_regexp
from fastjsonschema import JsonSchemaException


REGEX_PATTERNS = {
    "uri_re_pattern": re.compile('^\\w+:(\\/?\\/?)[^\\s]+$')
}

__version__ = "1.6"
NoneType = type(None)

def validate_http_json_schema_org_draft_06_schema(data):
    if not isinstance(data, (dict, bool)):
        raise JsonSchemaException("data must be object or boolean")
    if isinstance(data, dict):
        data_keys = set(data.keys())
        if "$id" in data_keys:
            data_keys.remove("$id")
            data_id = data["$id"]
            if not isinstance(data_id, (str)):
                raise JsonSchemaException("data.$id must be string")
            if isinstance(data_id, str):
                if not is_valid_uri_reference(data_id):
                    raise JsonSchemaException("data.$id must be a valid uri-reference")
        if "$schema" in data_keys:
            data_keys.remove("$schema")
            data_schema = data["$schema"]
            if not isinstance(data_schema, (str)):
                raise JsonSchemaException("data.$schema must be string")
            if isinstance(data_schema, str):
                if not REGEX_PATTERNS["uri_re_pattern"].match(data_schema):
                    raise JsonSchemaException("data.$schema must be uri")
        if "$ref" in data_keys:
            data_keys.remove("$ref")
            data_ref = data["$ref"]
            if not isinstance(data_ref, (str)):
                raise JsonSchemaException("data.$ref must be string")
            if isinstance(data_ref, str):
                if not is_valid_uri_reference(data_ref):
                    raise JsonSchemaException("data.$ref must be a valid uri-reference")
        if "title" in data_keys:
            data_keys.remove("title")
            data_title = data["title"]
            if not isinstance(data_title, (str)):
                raise JsonSchemaException("data.title must be string")
        if "description" in data_keys:
            data_keys.remove("description")
            data_description = data["description"]
            if not isinstance(data_description, (str)):
                raise JsonSchemaException("data.description must be string")
        if "default" in data_keys:
            data_keys.remove("default")
            data_default = data["default"]
        if "examples" in data_keys:
            data_keys.remove("examples")
            data_examples = data["examples"]
            if not isinstance(data_examples, (list)):
                raise JsonSchemaException("data.examples must be array")
            if isinstance(data_examples, list):
                data_examples_len = len(data_examples)
        if "multipleOf" in data_keys:
            data_keys.remove("multipleOf")
            data_multipleOf = data["multipleOf"]
            if not isinstance(data_multipleOf, (int, float)) or isinstance(data_multipleOf, bool):
                raise JsonSchemaException("data.multipleOf must be number")
            if isinstance(data_multipleOf, (int, float)):
                if data_multipleOf <= 0:
                    raise JsonSchemaException("data.multipleOf must be bigger than 0")
        if "maximum" in data_keys:
            data_keys.remove("maximum")
            data_maximum = data["maximum"]
            if not isinstance(data_maximum, (int, float)) or isinstance(data_maximum, bool):
                raise JsonSchemaException("data.maximum must be number")
        if "exclusiveMaximum" in data_keys:
            data_keys.remove("exclusiveMaximum")
            data_exclusiveMaximum = data["exclusiveMaximum"]
            if not isinstance(data_exclusiveMaximum, (int, float)) or isinstance(data_exclusiveMaximum, bool):
                raise JsonSchemaException("data.exclusiveMaximum must be number")
        if "minimum" in data_keys:
            data_keys.remove("minimum")
            data_minimum = data["minimum"]
            if not isinstance(data_minimum, (int, float)) or isinstance(data_minimum, bool):
                raise JsonSchemaException("data.minimum must be number")
        if "exclusiveMinimum" in data_keys:
            data_keys.remove("exclusiveMinimum")
            data_exclusiveMinimum = data["exclusiveMinimum"]
            if not isinstance(data_exclusiveMinimum, (int, float)) or isinstance(data_exclusiveMinimum, bool):
                raise JsonSchemaException("data.exclusiveMinimum must be number")
        if "maxLength" in data_keys:
            data_keys.remove("maxLength")
            data_maxLength = data["maxLength"]
            validate_http_json_schema_org_draft_06_schema_definitions_nonnegativeinteger(data_maxLength)
        if "minLength" in data_keys:
            data_keys.remove("minLength")
            data_minLength = data["minLength"]
            validate_http_json_schema_org_draft_06_schema_definitions_nonnegativeintegerdefault0(data_minLength)
        if "pattern" in data_keys:
            data_keys.remove("pattern")
            data_pattern = data["pattern"]
            if not isinstance(data_pattern, (str)):
                raise JsonSchemaException("data.pattern must be string")
            if isinstance(data_pattern, str):
                if not is_valid_regexp(data_pattern):
                    raise JsonSchemaException("data.pattern must be a valid regex")
        if "additionalItems" in data_keys:
            data_keys.remove("additionalItems")
            data_additionalItems = data["additionalItems"]
            validate_http_json_schema_org_draft_06_schema(data_additionalItems)
        if "items" in data_keys:
            data_keys.remove("items")
            data_items = data["items"]
            data_items_any_of_count = 0
            if not data_items_any_of_count:
                try:
                    validate_http_json_schema_org_draft_06_schema(data_items)
                    data_items_any_of_count += 1
                except JsonSchemaException: pass
            if not data_items_any_of_count:
                try:
                    validate_http_json_schema_org_draft_06_schema_definitions_schemaarray(data_items)
                    data_items_any_of_count += 1
                except JsonSchemaException: pass
            if not data_items_any_of_count:
                raise JsonSchemaException("data.items must be valid by one of anyOf definition")
        else: data["items"] = {}
        if "maxItems" in data_keys:
            data_keys.remove("maxItems")
            data_maxItems = data["maxItems"]
            validate_http_json_schema_org_draft_06_schema_definitions_nonnegativeinteger(data_maxItems)
        if "minItems" in data_keys:
            data_keys.remove("minItems")
            data_minItems = data["minItems"]
            validate_http_json_schema_org_draft_06_schema_definitions_nonnegativeintegerdefault0(data_minItems)
        if "uniqueItems" in data_keys:
            data_keys.remove("uniqueItems")
            data_uniqueItems = data["uniqueItems"]
            if not isinstance(data_uniqueItems, (bool)):
                raise JsonSchemaException("data.uniqueItems must be boolean")
        else: data["uniqueItems"] = False
        if "contains" in data_keys:
            data_keys.remove("contains")
            data_contains = data["contains"]
            validate_http_json_schema_org_draft_06_schema(data_contains)
        if "maxProperties" in data_keys:
            data_keys.remove("maxProperties")
            data_maxProperties = data["maxProperties"]
            validate_http_json_schema_org_draft_06_schema_definitions_nonnegativeinteger(data_maxProperties)
        if "minProperties" in data_keys:
            data_keys.remove("minProperties")
            data_minProperties = data["minProperties"]
            validate_http_json_schema_org_draft_06_schema_definitions_nonnegativeintegerdefault0(data_minProperties)
        if "required" in data_keys:
            data_keys.remove("required")
            data_required = data["required"]
            validate_http_json_schema_org_draft_06_schema_definitions_stringarray(data_required)
        if "additionalProperties" in data_keys:
            data_keys.remove("additionalProperties")
            data_additionalProperties = data["additionalProperties"]
            validate_http_json_schema_org_draft_06_schema(data_additionalProperties)
        if "definitions" in data_keys:
            data_keys.remove("definitions")
            data_definitions = data["definitions"]
            if not isinstance(data_definitions, (dict)):
                raise JsonSchemaException("data.definitions must be object")
            if isinstance(data_definitions, dict):
                data_definitions_keys = set(data_definitions.keys())
                for data_definitions_key in data_definitions_keys:
                    if data_definitions_key not in "dict_keys([])":
                        data_definitions_value = data_definitions.get(data_definitions_key)
                        validate_http_json_schema_org_draft_06_schema(data_definitions_value)
        else: data["definitions"] = {}
        if "properties" in data_keys:
            data_keys.remove("properties")
            data_properties = data["properties"]
            if not isinstance(data_properties, (dict)):
                raise JsonSchemaException("data.properties must be object")
            if isinstance(data_properties, dict):
                data_properties_keys = set(data_properties.keys())
                for data_properties_key in data_properties_keys:
                    if data_properties_key not in "dict_keys([])":
                        data_properties_value = data_properties.get(data_properties_key)
                        validate_http_json_schema_org_draft_06_schema(data_properties_value)
        else: data["properties"] = {}
        if "patternProperties" in data_keys:
            data_keys.remove("patternProperties")
            data_patternProperties = data["patternProperties"]
            if not isinstance(data_patternProperties, (dict)):
                raise JsonSchemaException("data.patternProperties must be object")
            if isinstance(data_patternProperties, dict):
                data_patternProperties_keys = set(data_patternProperties.keys())
                for data_patternProperties_key in data_patternProperties_keys:
                    if data_patternProperties_key not in "dict_keys([])":
                        data_patternProperties_value = data_patternProperties.get(data_patternProperties_key)
                        validate_http_json_schema_org_draft_06_schema(data_patternProperties_value)
        else: data["patternProperties"] = {}
        if "dependencies" in data_keys:
            data_keys.remove("dependencies")
            data_dependencies = data["dependencies"]
            if not isinstance(data_dependencies, (dict)):
                raise JsonSchemaException("data.dependencies must be object")
            if isinstance(data_dependencies, dict):
                data_dependencies_keys = set(data_dependencies.keys())
                for data_dependencies_key in data_dependencies_keys:
                    if data_dependencies_key not in "dict_keys([])":
                        data_dependencies_value = data_dependencies.get(data_dependencies_key)
                        data_dependencies_value_any_of_count = 0
                        if not data_dependencies_value_any_of_count:
                            try:
                                validate_http_json_schema_org_draft_06_schema(data_dependencies_value)
                                data_dependencies_value_any_of_count += 1
                            except JsonSchemaException: pass
                        if not data_dependencies_value_any_of_count:
                            try:
                                validate_http_json_schema_org_draft_06_schema_definitions_stringarray(data_dependencies_value)
                                data_dependencies_value_any_of_count += 1
                            except JsonSchemaException: pass
                        if not data_dependencies_value_any_of_count:
                            raise JsonSchemaException(""+"data.dependencies.{data_dependencies_key}".format(**locals())+" must be valid by one of anyOf definition")
        if "propertyNames" in data_keys:
            data_keys.remove("propertyNames")
            data_propertyNames = data["propertyNames"]
            validate_http_json_schema_org_draft_06_schema(data_propertyNames)
        if "const" in data_keys:
            data_keys.remove("const")
            data_const = data["const"]
        if "enum" in data_keys:
            data_keys.remove("enum")
            data_enum = data["enum"]
            if not isinstance(data_enum, (list)):
                raise JsonSchemaException("data.enum must be array")
            if isinstance(data_enum, list):
                data_enum_len = len(data_enum)
                if data_enum_len < 1:
                    raise JsonSchemaException("data.enum must contain at least 1 items")
            if data_enum_len > len(set(str(x) for x in data_enum)):
                raise JsonSchemaException("data.enum must contain unique items")
        if "type" in data_keys:
            data_keys.remove("type")
            data_type = data["type"]
            data_type_any_of_count = 0
            if not data_type_any_of_count:
                try:
                    validate_http_json_schema_org_draft_06_schema_definitions_simpletypes(data_type)
                    data_type_any_of_count += 1
                except JsonSchemaException: pass
            if not data_type_any_of_count:
                try:
                    if not isinstance(data_type, (list)):
                        raise JsonSchemaException("data.type must be array")
                    if isinstance(data_type, list):
                        data_type_len = len(data_type)
                        if data_type_len < 1:
                            raise JsonSchemaException("data.type must contain at least 1 items")
                    if data_type_len > len(set(str(x) for x in data_type)):
                        raise JsonSchemaException("data.type must contain unique items")
                    if isinstance(data_type, list):
                        for data_type_x, data_type_item in enumerate(data_type):
                            validate_http_json_schema_org_draft_06_schema_definitions_simpletypes(data_type_item)
                    data_type_any_of_count += 1
                except JsonSchemaException: pass
            if not data_type_any_of_count:
                raise JsonSchemaException("data.type must be valid by one of anyOf definition")
        if "format" in data_keys:
            data_keys.remove("format")
            data_format = data["format"]
            if not isinstance(data_format, (str)):
                raise JsonSchemaException("data.format must be string")
        if "allOf" in data_keys:
            data_keys.remove("allOf")
            data_allOf = data["allOf"]
            validate_http_json_schema_org_draft_06_schema_definitions_schemaarray(data_allOf)
        if "anyOf" in data_keys:
            data_keys.remove("anyOf")
            data_anyOf = data["anyOf"]
            validate_http_json_schema_org_draft_06_schema_definitions_schemaarray(data_anyOf)
        if "oneOf" in data_keys:
            data_keys.remove("oneOf")
            data_oneOf = data["oneOf"]
            validate_http_json_schema_org_draft_06_schema_definitions_schemaarray(data_oneOf)
        if "not" in data_keys:
            data_keys.remove("not")
            data_not = data["not"]
            validate_http_json_schema_org_draft_06_schema(data_not)
    return data

def validate_http_json_schema_org_draft_06_schema_definitions_simpletypes(data):
    if data not in ['array', 'boolean', 'integer', 'null', 'number', 'object', 'string']:
        raise JsonSchemaException("data must be one of ['array', 'boolean', 'integer', 'null', 'number', 'object', 'string']")
    return data

def validate_http_json_schema_org_draft_06_schema_definitions_stringarray(data):
    if not isinstance(data, (list)):
        raise JsonSchemaException("data must be array")
    data_len = len(data)
    if data_len > len(set(str(x) for x in data)):
        raise JsonSchemaException("data must contain unique items")
    if isinstance(data, list):
        for data_x, data_item in enumerate(data):
            if not isinstance(data_item, (str)):
                raise JsonSchemaException(""+"data[{data_x}]".format(**locals())+" must be string")
    return data

def validate_http_json_schema_org_draft_06_schema_definitions_schemaarray(data):
    if not isinstance(data, (list)):
        raise JsonSchemaException("data must be array")
    if isinstance(data, list):
        data_len = len(data)
        if data_len < 1:
            raise JsonSchemaException("data must contain at least 1 items")
    if isinstance(data, list):
        for data_x, data_item in enumerate(data):
            validate_http_json_schema_org_draft_06_schema(data_item)
    return data

def validate_http_json_schema_org_draft_06_schema_definitions_nonnegativeintegerdefault0(data):
    validate_http_json_schema_org_draft_06_schema_definitions_nonnegativeinteger(data)
    return data

def validate_http_json_schema_org_draft_06_schema_definitions_nonnegativeinteger(data):
    if not isinstance(data, (int)) and not (isinstance(data, float) and data.is_integer()) or isinstance(data, bool):
        raise JsonSchemaException("data must be integer")
    if isinstance(data, (int, float)):
        if data < 0:
            raise JsonSchemaException("data must be bigger than or equal to 0")
    return data
