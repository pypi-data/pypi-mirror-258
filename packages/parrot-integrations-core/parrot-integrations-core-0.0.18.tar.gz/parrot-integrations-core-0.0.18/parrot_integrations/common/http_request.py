def get_schema():
    return dict(
        name='Http Request',
        description='Make an HTTP Request',
        is_expandable=False,
        schema=dict(
            type='object',
            additionalProperties=False,
            description='Make an HTTP Request',
            required=['inputs', 'outputs'],
            properties=dict(
                expand_results=dict(
                    type='boolean',
                    default=False,
                    enum=[False]
                ),
                inputs=dict(
                    type='object',
                    additionalProperties=False,
                    required=['method', 'url'],
                    properties=dict(
                        method=dict(
                            type='string',
                        ),
                        url=dict(
                            type='string',
                            format='uri'
                        ),
                        url_params=dict(
                            type='object'
                        ),
                        json_payload=dict(
                            type='object',
                        )
                    )
                ),
                outputs=dict(
                    type='object',
                    required=[
                        'status_code'
                    ],
                    properties=dict(
                        status_code=dict(
                            type='integer',
                        ),
                        json=dict(
                            type='object',
                        ),
                        text=dict(
                            type='string',
                        ),
                    )
                )
            )
        )
    )


def process(inputs, **kwargs):
    import requests

    resp = requests.request(
        method=inputs['method'],
        url=inputs['url'],
        params=dict(
            (param['key'], param['value']) for param in inputs['url_params']
        ) if inputs.get('url_params') else None,
        json=dict(
            (param['key'], param['value']) for param in inputs['json_payload']
        ) if inputs.get('json_payload') else None
    )
    response = dict(
        status_code=resp.status_code,
        text=resp.text
    )
    try:
        response['json'] = resp.json()
    except:
        pass
    return response
