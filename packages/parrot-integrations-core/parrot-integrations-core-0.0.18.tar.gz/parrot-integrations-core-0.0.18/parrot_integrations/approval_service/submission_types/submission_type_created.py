from parrot_integrations.approval_service.submission_types import OBJECT_SCHEMA
from parrot_integrations.core import generate_trigger_schema, trigger_object


def get_schema():
    return generate_trigger_schema(object_type='submission_type', object_schema=OBJECT_SCHEMA, status='created')


def process(inputs, **kwargs):
    return trigger_object(inputs=inputs)
