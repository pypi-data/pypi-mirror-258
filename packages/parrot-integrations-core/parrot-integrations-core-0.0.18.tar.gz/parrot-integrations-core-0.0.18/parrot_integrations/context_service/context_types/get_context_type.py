from parrot_integrations.context_service.context_types import OBJECT_SCHEMA
from parrot_integrations.core import get_object, generate_get_schema


def get_schema():
    return generate_get_schema(object_type='context_type', object_schema=OBJECT_SCHEMA)


def process(inputs, integration, token, account_uuid, **kwargs):
    return get_object(integration=integration, object_type='context_type', object_uuid=inputs['context_type_uuid'],
                      token=token, account_uuid=account_uuid)
