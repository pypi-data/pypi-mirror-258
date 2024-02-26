from parrot_integrations.core import search_objects, generate_search_schema
from parrot_integrations.workflow_service.workflows import OBJECT_SCHEMA


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
        workflow_uuids=dict(
            type='array',
            items=dict(
                type='string',
                format='uuid',
                description='The workflow UUIDs to search for'
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
    return generate_search_schema(plural_object_type='workflows', object_schema=OBJECT_SCHEMA,
                                  search_schema=search_schema)


def process(inputs, integration, token, account_uuid, **kwargs):
    return search_objects(
        integration=integration,
        plural_object_type='workflows',
        search_parameters=inputs,
        token=token,
        account_uuid=account_uuid
    )
