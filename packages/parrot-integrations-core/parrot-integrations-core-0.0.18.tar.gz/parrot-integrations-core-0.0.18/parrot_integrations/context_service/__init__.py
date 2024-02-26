from .context import *
from .context_types import *


def get_integration_schema():
    return dict(
        type='object',
        additionalProperties=False,
        description='Context Service integration',
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
                        description='URL of the Context Service',
                        default='https://api.example.com/context/v1/'
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
