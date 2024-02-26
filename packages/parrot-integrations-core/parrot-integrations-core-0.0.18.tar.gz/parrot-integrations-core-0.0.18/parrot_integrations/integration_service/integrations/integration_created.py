from parrot_integrations.core import generate_trigger_schema, trigger_object
from parrot_integrations.integration_service.integrations import OBJECT_SCHEMA


def get_schema():
    return generate_trigger_schema(object_type='integration', object_schema=OBJECT_SCHEMA, status='created')


def process(inputs, **kwargs):
    return trigger_object(inputs=inputs)
