from parrot_integrations.context_service.context import OBJECT_SCHEMA
from parrot_integrations.core.schemas import format_input_schema


def get_schema():
    return dict(
        name='Upload Context File',
        description='Upload a file to an existing context',
        is_trigger=False,
        schema=dict(
            type='object',
            additionalProperties=False,
            required=['inputs', 'outputs'],
            properties=dict(
                inputs=format_input_schema(
                    input_schema=dict(
                        type='object',
                        additionalProperties=False,
                        required=['context_uuid', 'file'],
                        properties=dict(
                            context_uuid=dict(
                                type='string',
                                format='uuid'
                            ),
                            file=dict(
                                type='string',
                                format='uri'
                            )
                        )
                    )
                ),
                outputs=OBJECT_SCHEMA
            )
        )
    )


def process(integration, inputs, account_uuid, **kwargs):
    return inputs
