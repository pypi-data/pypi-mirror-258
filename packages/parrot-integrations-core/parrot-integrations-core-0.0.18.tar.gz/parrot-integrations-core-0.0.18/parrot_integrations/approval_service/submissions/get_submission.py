from parrot_integrations.approval_service.submissions import OBJECT_SCHEMA
from parrot_integrations.core import get_object, generate_get_schema


def get_schema():
    return generate_get_schema(object_type='submission', object_schema=OBJECT_SCHEMA)


def process(inputs, integration, token, account_uuid, **kwargs):
    return get_object(integration=integration, object_type='submission', object_uuid=inputs['submission_uuid'],
                      token=token, account_uuid=account_uuid)
