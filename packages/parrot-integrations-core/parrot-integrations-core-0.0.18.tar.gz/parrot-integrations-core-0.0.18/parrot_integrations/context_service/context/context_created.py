from parrot_integrations.context_service.context import OBJECT_SCHEMA
from parrot_integrations.core import generate_trigger_schema, trigger_object


def get_schema():
    return generate_trigger_schema(object_type='context', object_schema=OBJECT_SCHEMA, status='created')


def process(inputs, **kwargs):
    return trigger_object(inputs=inputs)
