from parrot_integrations.approval_service.submission_types import OBJECT_SCHEMA
from parrot_integrations.core import create_object, generate_create_schema


def get_schema():
    return generate_create_schema(object_type='submission_type', object_schema=OBJECT_SCHEMA)


def process(inputs, integration, token, account_uuid, **kwargs):
    return create_object(integration=integration, object_type='submission_type', data=inputs, token=token,
                         account_uuid=account_uuid)
