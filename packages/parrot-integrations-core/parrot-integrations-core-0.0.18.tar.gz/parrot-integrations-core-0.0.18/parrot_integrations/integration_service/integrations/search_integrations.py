from parrot_integrations.core import search_objects, generate_search_schema
from parrot_integrations.integration_service.integrations import OBJECT_SCHEMA


def get_schema():
    search_schema = dict(
        account_uuids=dict(
            type='array',
            items=dict(
                type='string',
                format='uuid',
                description='The account UUIDs to search for'
            )
        ),
        integration_type_uuids=dict(
            type='array',
            items=dict(
                type='string',
                format='uuid',
                description='The integration type UUIDs to search for'
            )
        ),
        is_active=dict(
            type=['null', 'boolean'],
            default=True
        ),
        is_visible=dict(
            type=['null', 'boolean'],
            default=True
        )
    )
    return generate_search_schema(plural_object_type='integrations', object_schema=OBJECT_SCHEMA,
                                  search_schema=search_schema)


def process(inputs, integration, token, account_uuid, **kwargs):
    return search_objects(
        integration=integration,
        plural_object_type='integrations',
        search_parameters=inputs,
        token=token,
        account_uuid=account_uuid
    )
