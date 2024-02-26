from parrot_integrations.approval_service.submissions import OBJECT_SCHEMA
from parrot_integrations.core import generate_trigger_schema, trigger_object


def get_schema():
    return generate_trigger_schema(object_type='submission', object_schema=OBJECT_SCHEMA, status='updated')


def process(inputs, **kwargs):
    return trigger_object(inputs=inputs)
