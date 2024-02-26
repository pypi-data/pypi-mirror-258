from .account_types import *
from .accounts import *


def get_integration_schema():
    return dict(
        type='object',
        additionalProperties=False,
        description='Account Service integration',
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
                        description='URL of the Account Service',
                        default='https://api.example.com/account/v1/'
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
