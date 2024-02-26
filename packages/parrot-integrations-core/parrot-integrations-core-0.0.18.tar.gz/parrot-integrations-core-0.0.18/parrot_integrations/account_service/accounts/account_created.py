from parrot_integrations.account_service.accounts import OBJECT_SCHEMA
from parrot_integrations.core import generate_trigger_schema, trigger_object


def get_schema():
    return generate_trigger_schema(object_type='account', object_schema=OBJECT_SCHEMA, status='created')


def process(inputs, **kwargs):
    return trigger_object(inputs=inputs)
