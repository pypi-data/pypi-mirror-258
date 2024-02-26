from parrot_integrations.core import generate_trigger_schema, trigger_object
from parrot_integrations.workflow_service.workflows import OBJECT_SCHEMA


def get_schema():
    return generate_trigger_schema(object_type='workflow', object_schema=OBJECT_SCHEMA, status='created')


def process(inputs, **kwargs):
    return trigger_object(inputs=inputs)
