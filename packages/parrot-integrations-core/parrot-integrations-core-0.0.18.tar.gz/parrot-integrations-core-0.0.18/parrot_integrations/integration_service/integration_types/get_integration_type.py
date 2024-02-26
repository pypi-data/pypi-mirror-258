from parrot_integrations.core import get_object, generate_get_schema
from parrot_integrations.integration_service.integration_types import OBJECT_SCHEMA


def get_schema():
    return generate_get_schema(object_type='integration_type', object_schema=OBJECT_SCHEMA)


def process(inputs, integration, token, account_uuid, **kwargs):
    return get_object(integration=integration, object_type='integration_type',
                      object_uuid=inputs['integration_type_uuid'], token=token, account_uuid=account_uuid)
