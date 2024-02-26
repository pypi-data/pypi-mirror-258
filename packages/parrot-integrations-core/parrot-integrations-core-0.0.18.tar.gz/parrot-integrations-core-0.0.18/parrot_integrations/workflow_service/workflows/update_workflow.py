from parrot_integrations.core import generate_update_schema, update_object
from parrot_integrations.workflow_service.workflows import OBJECT_SCHEMA


def get_schema():
    return generate_update_schema(object_type='workflow', object_schema=OBJECT_SCHEMA, update_fields=[
        'name',
        'description',
        'is_inherited',
        'status_id',
        'nodes',
        'edges',
    ])


def process(inputs, integration, token, account_uuid, **kwargs):
    return update_object(integration=integration, account_uuid=account_uuid, object_type='workflow',
                         object_uuid=inputs['workflow_uuid'], data=inputs['attributes'], token=token)
