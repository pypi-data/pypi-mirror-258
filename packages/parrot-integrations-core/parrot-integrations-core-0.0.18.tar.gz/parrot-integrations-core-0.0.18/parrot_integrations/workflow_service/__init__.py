from .workflows import *


def get_integration_schema():
    return dict(
        type='object',
        additionalProperties=False,
        description='Workflow Service integration',
        required=['extra_attributes', 'credentials'],
        properties=dict(
            extra_attributes=dict(
                type='object',
                additionalProperties=False,
                required=[
                    'base_url'
                ],
                properties=dict(
                    base_url=dict(
                        type='string',
                        description='URL of the Workflow Service',
                        default='https://api.example.com/workflow/v1/'
                    )
                )
            ),
            credentials=dict(
                type='object',
                additionalProperties=False,
                required=[],
                properties=dict()
            )
        )
    )


def connect(extra_attributes, credentials):
    return dict()
