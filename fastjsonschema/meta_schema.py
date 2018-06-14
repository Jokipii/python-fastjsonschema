draft_04_meta_schema = {
    'id': 'http://json-schema.org/draft-04/schema#',
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'default': {},
    'definitions': {
        'positiveInteger': {
            'minimum': 0,
            'type': 'integer'
        },
        'positiveIntegerDefault0': {
            'allOf': [{
                '$ref': '#/definitions/positiveInteger'
            }, {
                'default': 0
            }]
        },
        'schemaArray': {
            'items': {
                '$ref': '#'
            },
            'minItems': 1,
            'type': 'array'
        },
        'simpleTypes': {
            'enum': [
                'array', 'boolean', 'integer', 'null', 'number', 'object',
                'string'
            ]
        },
        'stringArray': {
            'items': {
                'type': 'string'
            },
            'minItems': 1,
            'type': 'array',
            'uniqueItems': True
        }
    },
    'dependencies': {
        'exclusiveMaximum': ['maximum'],
        'exclusiveMinimum': ['minimum']
    },
    'description': 'Core schema meta-schema',
    'properties': {
        '$schema': {
            'format': 'uri',
            'type': 'string'
        },
        'additionalItems': {
            'anyOf': [{
                'type': 'boolean'
            }, {
                '$ref': '#'
            }],
            'default': {}
        },
        'additionalProperties': {
            'anyOf': [{
                'type': 'boolean'
            }, {
                '$ref': '#'
            }],
            'default': {}
        },
        'allOf': {
            '$ref': '#/definitions/schemaArray'
        },
        'anyOf': {
            '$ref': '#/definitions/schemaArray'
        },
        'default': {},
        'definitions': {
            'additionalProperties': {
                '$ref': '#'
            },
            'default': {},
            'type': 'object'
        },
        'dependencies': {
            'additionalProperties': {
                'anyOf': [{
                    '$ref': '#'
                }, {
                    '$ref': '#/definitions/stringArray'
                }]
            },
            'type': 'object'
        },
        'description': {
            'type': 'string'
        },
        'enum': {
            'minItems': 1,
            'type': 'array',
            'uniqueItems': True
        },
        'exclusiveMaximum': {
            'default': False,
            'type': 'boolean'
        },
        'exclusiveMinimum': {
            'default': False,
            'type': 'boolean'
        },
        'format': {
            'type': 'string'
        },
        'id': {
            'format': 'uri',
            'type': 'string'
        },
        'items': {
            'anyOf': [{
                '$ref': '#'
            }, {
                '$ref': '#/definitions/schemaArray'
            }],
            'default': {}
        },
        'maxItems': {
            '$ref': '#/definitions/positiveInteger'
        },
        'maxLength': {
            '$ref': '#/definitions/positiveInteger'
        },
        'maxProperties': {
            '$ref': '#/definitions/positiveInteger'
        },
        'maximum': {
            'type': 'number'
        },
        'minItems': {
            '$ref': '#/definitions/positiveIntegerDefault0'
        },
        'minLength': {
            '$ref': '#/definitions/positiveIntegerDefault0'
        },
        'minProperties': {
            '$ref': '#/definitions/positiveIntegerDefault0'
        },
        'minimum': {
            'type': 'number'
        },
        'multipleOf': {
            'exclusiveMinimum': True,
            'minimum': 0,
            'type': 'number'
        },
        'not': {
            '$ref': '#'
        },
        'oneOf': {
            '$ref': '#/definitions/schemaArray'
        },
        'pattern': {
            'format': 'regex',
            'type': 'string'
        },
        'patternProperties': {
            'additionalProperties': {
                '$ref': '#'
            },
            'default': {},
            'type': 'object'
        },
        'properties': {
            'additionalProperties': {
                '$ref': '#'
            },
            'default': {},
            'type': 'object'
        },
        'required': {
            '$ref': '#/definitions/stringArray'
        },
        'title': {
            'type': 'string'
        },
        'type': {
            'anyOf': [{
                '$ref': '#/definitions/simpleTypes'
            }, {
                'items': {
                    '$ref': '#/definitions/simpleTypes'
                },
                'minItems': 1,
                'type': 'array',
                'uniqueItems': True
            }]
        },
        'uniqueItems': {
            'default': False,
            'type': 'boolean'
        }
    },
    'type': 'object'
}

draft_06_meta_schema = {
    '$id': 'http://json-schema.org/draft-06/schema#',
    '$schema': 'http://json-schema.org/draft-06/schema#',
    'default': {},
    'definitions': {
        'nonNegativeInteger': {
            'minimum': 0,
            'type': 'integer'
        },
        'nonNegativeIntegerDefault0': {
            'allOf': [{
                '$ref': '#/definitions/nonNegativeInteger'
            }, {
                'default': 0
            }]
        },
        'schemaArray': {
            'items': {
                '$ref': '#'
            },
            'minItems': 1,
            'type': 'array'
        },
        'simpleTypes': {
            'enum': [
                'array', 'boolean', 'integer', 'null', 'number', 'object',
                'string'
            ]
        },
        'stringArray': {
            'default': [],
            'items': {
                'type': 'string'
            },
            'type': 'array',
            'uniqueItems': True
        }
    },
    'properties': {
        '$id': {
            'format': 'uri-reference',
            'type': 'string'
        },
        '$ref': {
            'format': 'uri-reference',
            'type': 'string'
        },
        '$schema': {
            'format': 'uri',
            'type': 'string'
        },
        'additionalItems': {
            '$ref': '#'
        },
        'additionalProperties': {
            '$ref': '#'
        },
        'allOf': {
            '$ref': '#/definitions/schemaArray'
        },
        'anyOf': {
            '$ref': '#/definitions/schemaArray'
        },
        'const': {},
        'contains': {
            '$ref': '#'
        },
        'default': {},
        'definitions': {
            'additionalProperties': {
                '$ref': '#'
            },
            'default': {},
            'type': 'object'
        },
        'dependencies': {
            'additionalProperties': {
                'anyOf': [{
                    '$ref': '#'
                }, {
                    '$ref': '#/definitions/stringArray'
                }]
            },
            'type': 'object'
        },
        'description': {
            'type': 'string'
        },
        'enum': {
            'minItems': 1,
            'type': 'array',
            'uniqueItems': True
        },
        'examples': {
            'items': {},
            'type': 'array'
        },
        'exclusiveMaximum': {
            'type': 'number'
        },
        'exclusiveMinimum': {
            'type': 'number'
        },
        'format': {
            'type': 'string'
        },
        'items': {
            'anyOf': [{
                '$ref': '#'
            }, {
                '$ref': '#/definitions/schemaArray'
            }],
            'default': {}
        },
        'maxItems': {
            '$ref': '#/definitions/nonNegativeInteger'
        },
        'maxLength': {
            '$ref': '#/definitions/nonNegativeInteger'
        },
        'maxProperties': {
            '$ref': '#/definitions/nonNegativeInteger'
        },
        'maximum': {
            'type': 'number'
        },
        'minItems': {
            '$ref': '#/definitions/nonNegativeIntegerDefault0'
        },
        'minLength': {
            '$ref': '#/definitions/nonNegativeIntegerDefault0'
        },
        'minProperties': {
            '$ref': '#/definitions/nonNegativeIntegerDefault0'
        },
        'minimum': {
            'type': 'number'
        },
        'multipleOf': {
            'exclusiveMinimum': 0,
            'type': 'number'
        },
        'not': {
            '$ref': '#'
        },
        'oneOf': {
            '$ref': '#/definitions/schemaArray'
        },
        'pattern': {
            'format': 'regex',
            'type': 'string'
        },
        'patternProperties': {
            'additionalProperties': {
                '$ref': '#'
            },
            'default': {},
            'type': 'object'
        },
        'properties': {
            'additionalProperties': {
                '$ref': '#'
            },
            'default': {},
            'type': 'object'
        },
        'propertyNames': {
            '$ref': '#'
        },
        'required': {
            '$ref': '#/definitions/stringArray'
        },
        'title': {
            'type': 'string'
        },
        'type': {
            'anyOf': [{
                '$ref': '#/definitions/simpleTypes'
            }, {
                'items': {
                    '$ref': '#/definitions/simpleTypes'
                },
                'minItems': 1,
                'type': 'array',
                'uniqueItems': True
            }]
        },
        'uniqueItems': {
            'default': False,
            'type': 'boolean'
        }
    },
    'title': 'Core schema meta-schema',
    'type': ['object', 'boolean']
}

draft_07_meta_schema = {
    '$id': 'http://json-schema.org/draft-07/schema#',
    '$schema': 'http://json-schema.org/draft-07/schema#',
    'default': True,
    'definitions': {
        'nonNegativeInteger': {
            'minimum': 0,
            'type': 'integer'
        },
        'nonNegativeIntegerDefault0': {
            'allOf': [{
                '$ref': '#/definitions/nonNegativeInteger'
            }, {
                'default': 0
            }]
        },
        'schemaArray': {
            'items': {
                '$ref': '#'
            },
            'minItems': 1,
            'type': 'array'
        },
        'simpleTypes': {
            'enum': [
                'array', 'boolean', 'integer', 'null', 'number', 'object',
                'string'
            ]
        },
        'stringArray': {
            'default': [],
            'items': {
                'type': 'string'
            },
            'type': 'array',
            'uniqueItems': True
        }
    },
    'properties': {
        '$comment': {
            'type': 'string'
        },
        '$id': {
            'format': 'uri-reference',
            'type': 'string'
        },
        '$ref': {
            'format': 'uri-reference',
            'type': 'string'
        },
        '$schema': {
            'format': 'uri',
            'type': 'string'
        },
        'additionalItems': {
            '$ref': '#'
        },
        'additionalProperties': {
            '$ref': '#'
        },
        'allOf': {
            '$ref': '#/definitions/schemaArray'
        },
        'anyOf': {
            '$ref': '#/definitions/schemaArray'
        },
        'const': True,
        'contains': {
            '$ref': '#'
        },
        'contentEncoding': {
            'type': 'string'
        },
        'contentMediaType': {
            'type': 'string'
        },
        'default': True,
        'definitions': {
            'additionalProperties': {
                '$ref': '#'
            },
            'default': {},
            'type': 'object'
        },
        'dependencies': {
            'additionalProperties': {
                'anyOf': [{
                    '$ref': '#'
                }, {
                    '$ref': '#/definitions/stringArray'
                }]
            },
            'type': 'object'
        },
        'description': {
            'type': 'string'
        },
        'else': {
            '$ref': '#'
        },
        'enum': {
            'items': True,
            'minItems': 1,
            'type': 'array',
            'uniqueItems': True
        },
        'examples': {
            'items': True,
            'type': 'array'
        },
        'exclusiveMaximum': {
            'type': 'number'
        },
        'exclusiveMinimum': {
            'type': 'number'
        },
        'format': {
            'type': 'string'
        },
        'if': {
            '$ref': '#'
        },
        'items': {
            'anyOf': [{
                '$ref': '#'
            }, {
                '$ref': '#/definitions/schemaArray'
            }],
            'default': True
        },
        'maxItems': {
            '$ref': '#/definitions/nonNegativeInteger'
        },
        'maxLength': {
            '$ref': '#/definitions/nonNegativeInteger'
        },
        'maxProperties': {
            '$ref': '#/definitions/nonNegativeInteger'
        },
        'maximum': {
            'type': 'number'
        },
        'minItems': {
            '$ref': '#/definitions/nonNegativeIntegerDefault0'
        },
        'minLength': {
            '$ref': '#/definitions/nonNegativeIntegerDefault0'
        },
        'minProperties': {
            '$ref': '#/definitions/nonNegativeIntegerDefault0'
        },
        'minimum': {
            'type': 'number'
        },
        'multipleOf': {
            'exclusiveMinimum': 0,
            'type': 'number'
        },
        'not': {
            '$ref': '#'
        },
        'oneOf': {
            '$ref': '#/definitions/schemaArray'
        },
        'pattern': {
            'format': 'regex',
            'type': 'string'
        },
        'patternProperties': {
            'additionalProperties': {
                '$ref': '#'
            },
            'default': {},
            'propertyNames': {
                'format': 'regex'
            },
            'type': 'object'
        },
        'properties': {
            'additionalProperties': {
                '$ref': '#'
            },
            'default': {},
            'type': 'object'
        },
        'propertyNames': {
            '$ref': '#'
        },
        'readOnly': {
            'default': False,
            'type': 'boolean'
        },
        'required': {
            '$ref': '#/definitions/stringArray'
        },
        'then': {
            '$ref': '#'
        },
        'title': {
            'type': 'string'
        },
        'type': {
            'anyOf': [{
                '$ref': '#/definitions/simpleTypes'
            }, {
                'items': {
                    '$ref': '#/definitions/simpleTypes'
                },
                'minItems': 1,
                'type': 'array',
                'uniqueItems': True
            }]
        },
        'uniqueItems': {
            'default': False,
            'type': 'boolean'
        }
    },
    'title': 'Core schema meta-schema',
    'type': ['object', 'boolean']
}

meta_schemas = {
    'http://json-schema.org/draft-04/schema#': draft_04_meta_schema,
    'http://json-schema.org/draft-06/schema#': draft_06_meta_schema,
    'http://json-schema.org/draft-07/schema#': draft_07_meta_schema,
}
