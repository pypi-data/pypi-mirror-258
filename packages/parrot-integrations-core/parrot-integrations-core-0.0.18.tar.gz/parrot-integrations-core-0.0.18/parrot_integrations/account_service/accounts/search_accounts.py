from parrot_integrations.account_service.accounts import OBJECT_SCHEMA
from parrot_integrations.core import search_objects, generate_search_schema


def get_schema():
    search_schema = dict(
        account_type_uuids=dict(
            type='array',
            items=dict(
                type='string',
                format='uuid',
                description='The account type UUIDs to search for'
            )
        ),
        account_uuids=dict(
            type='array',
            items=dict(
                type='string',
                format='uuid',
                description='The account UUIDs to search for'
            )
        ),
        parent_account_uuids=dict(
            type='array',
            items=dict(
                type='string',
                format='uuid',
                description='The account UUIDs to search for'
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
    return generate_search_schema(plural_object_type='accounts', object_schema=OBJECT_SCHEMA,
                                  search_schema=search_schema)


def process(inputs, integration, token, account_uuid, **kwargs):
    account_uuids = inputs.get('account_uuids')
    account_type_uuids = inputs.get('account_type_uuids')
    parent_account_uuids = inputs.get('parent_account_uuids')
    search_parameters = dict(
        account_uuids=account_uuids,
        account_type_uuids=account_type_uuids,
        parent_account_uuids=parent_account_uuids
    )
    if parent_account_uuids is None and account_uuids is None and account_uuid is not None:
        search_parameters['parent_account_uuids'] = [account_uuid]

    return search_objects(
        integration=integration,
        plural_object_type='accounts',
        search_parameters=search_parameters,
        token=token,
        account_uuid=account_uuid
    )
