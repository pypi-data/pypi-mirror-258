from croniter import croniter


def get_schema():
    return dict(
        name='Crontab Scheduler',
        description='Trigger Jobs on a Schedule',
        is_trigger=True,
        schema=dict(
            type='object',
            additionalProperties=False,
            description='Trigger Jobs on a Schedule',
            required=['inputs', 'outputs'],
            properties=dict(
                inputs=dict(
                    type='object',
                    additionalProperties=False,
                    properties=dict(
                        expression=dict(
                            type='string',
                        )
                    )
                ),
                outputs=dict(
                    type='object',
                    required=['current_ts'],
                    properties=dict(
                        current_ts=dict(
                            type='number'
                        )
                    )
                ),
            )
        )
    )


def process(inputs, **kwargs):
    output = dict(
        current_ts=inputs['current_ts'].timestamp()
    )
    if croniter.match(inputs['expression'], inputs['current_ts']):
        return output
    else:
        return None
