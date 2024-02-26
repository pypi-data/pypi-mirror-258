import functools
from copy import deepcopy

TRANSFORMS_SCHEMA = dict(
    type="array",
    items={
        "type": "object",
        "additionalProperties": False,
        "required": ["operator", "arguments"],
        "properties": {
            "operator": {
                "type": "string"
            },
            "arguments": {
                "type": "object"
            }
        }
    }
)


@functools.cache
def get_operation_schema(integration_key, operation_key):
    from parrot_integrations.core.common import load_integration_module
    operation = load_integration_module(integration_key, operation_key)
    schema = operation.get_schema()
    schema['schema']['properties']['inputs'] = format_input_schema(
        input_schema=schema['schema']['properties']['inputs'])
    return schema


def generate_get_schema(object_type, object_schema):
    return dict(
        name=f'Get {object_type}',
        description=f'Get a single {object_type} by ID.',
        is_trigger=False,
        schema=dict(
            type='object',
            additionalProperties=False,
            required=['inputs'],
            properties=dict(
                inputs=dict(
                    type='object',
                    additionalProperties=False,
                    required=[f'{object_type}_uuid'],
                    properties={
                        f'{object_type}_uuid': dict(
                            type='string',
                            format='uuid'
                        )
                    }
                ),
                outputs=dict(
                    type='object',
                    additionalProperties=True,
                    required=[object_type, 'exists'],
                    properties={
                        object_type: object_schema,
                        "exists": dict(
                            type='boolean'
                        )
                    }
                ),
            )
        )
    )


def generate_create_schema(object_type, object_schema):
    object_schema = deepcopy(object_schema)
    return dict(
        name=f'Create {object_type}',
        description=f'Create a single {object_type}',
        is_trigger=False,
        schema=dict(
            type='object',
            additionalProperties=False,
            required=['inputs'],
            properties=dict(
                inputs=object_schema,
                outputs=dict(
                    type='object',
                    additionalProperties=True,
                    required=[object_type, 'created'],
                    properties={
                        object_type: object_schema,
                        "created": dict(
                            type='boolean'
                        )
                    }
                ),
            )
        )
    )


def generate_update_schema(object_type, object_schema, update_fields):
    object_schema = deepcopy(object_schema)
    update_schema = dict(
        type='object',
        additionalProperties=False,
        properties={f: object_schema['properties'][f] for f in update_fields}
    )
    return dict(
        name=f'Update {object_type}',
        description=f'Update a single {object_type}',
        is_trigger=False,
        schema=dict(
            type='object',
            additionalProperties=False,
            required=['inputs'],
            properties=dict(
                inputs=dict(
                    type='object',
                    additionalProperties=False,
                    required=[f'{object_type}_uuid', 'attributes'],
                    properties={
                        f'{object_type}_uuid': dict(
                            type='string',
                            format='uuid'
                        ),
                        'attributes': update_schema
                    }
                ),
                outputs=dict(
                    type='object',
                    additionalProperties=True,
                    required=[object_type, 'updated'],
                    properties={
                        object_type: object_schema,
                        "updated": dict(
                            type='boolean'
                        )
                    }
                ),
            )
        )
    )


def generate_search_schema(plural_object_type, object_schema, search_schema):
    return dict(
        name=f'Search {plural_object_type}',
        description=f'Search for {plural_object_type}',
        is_trigger=False,
        schema=dict(
            type='object',
            additionalProperties=False,
            required=['inputs'],
            properties=dict(
                inputs=dict(
                    type='object',
                    additionalProperties=False,
                    properties=search_schema
                ),
                outputs=dict(
                    type='object',
                    additionalProperties=True,
                    required=[plural_object_type],
                    properties={
                        plural_object_type: dict(
                            type='array',
                            items=object_schema,
                        )
                    }
                ),
            )
        )
    )


def generate_trigger_schema(object_type, object_schema, status):
    return dict(
        name=f'{object_type} {status} Trigger',
        description=f'Notify when a {object_type} is {status}',
        is_trigger=True,
        schema=dict(
            type='object',
            additionalProperties=False,
            required=['inputs'],
            properties=dict(
                inputs=dict(
                    type='object',
                    additionalProperties=False,
                    required=['record'],
                    properties=dict(
                        record=
                        dict(
                            oneOf=dict(
                                type='object',
                                required=['path'],
                                additionalProperties=False,
                                properties=dict(
                                    path=dict(
                                        type='string',
                                        enum=['record']
                                    )
                                )
                            )
                        )
                    )
                ),
                outputs=dict(
                    type='object',
                    additionalProperties=True,
                    required=[object_type],
                    properties={
                        object_type: object_schema
                    }
                ),
            )
        )
    )


def format_input_schema(input_schema):
    new_schema = input_schema
    if input_schema['type'] == 'object':
        if not input_schema.get('properties') and input_schema.get('additionalProperties', True):
            new_schema = dict(
                type='array',
                items=format_schema_value(field=None, include_key=True)
            )
        else:
            new_properties = dict()
            for k, v in input_schema['properties'].items():
                if v.get('readOnly'):
                    continue
                if v.get('type') == 'object':
                    new_properties[k] = format_input_schema(input_schema=v)
                elif v.get('type') == 'array':
                    new_properties[k] = v
                    new_properties[k]['items'] = format_input_schema(input_schema=v['items'])
                else:
                    new_properties[k] = format_schema_value(field=v)
            new_schema['properties'] = new_properties
    elif input_schema['type'] == 'array':
        new_schema['items'] = format_input_schema(input_schema=input_schema['items'])
    else:
        new_schema = format_schema_value(field=input_schema)
    return new_schema


def format_schema_value(field=None, include_key=False):
    if field is None:
        field = dict(
            type=['string', 'number', 'integer', 'boolean']
        )
    schema = dict(
        oneOf=[
            dict(
                type='object',
                additionalProperties=False,
                required=['path'],
                properties=dict(
                    path=dict(
                        type='string',
                    ),
                    default=field,
                    transforms=TRANSFORMS_SCHEMA
                )
            ),
            dict(
                type='object',
                additionalProperties=False,
                required=['value'],
                properties=dict(
                    value=field,
                    transforms=TRANSFORMS_SCHEMA
                )
            )
        ]
    )
    if include_key:
        schema['oneOf'][0]['required'].append('key')
        schema['oneOf'][0]['properties']['key'] = dict(type='string')
        schema['oneOf'][1]['required'].append('key')
        schema['oneOf'][1]['properties']['key'] = dict(type='string')
    return schema
