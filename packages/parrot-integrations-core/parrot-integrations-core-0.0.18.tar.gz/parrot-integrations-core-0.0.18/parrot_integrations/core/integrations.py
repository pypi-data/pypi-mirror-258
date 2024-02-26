from urllib.parse import urljoin

import requests

TRANSFORMS_SCHEMA = dict(
    type="array",
    items={
        "type": "object",
        "additionalProperties": False,
        "required": ["operator", "arguments"],
        "properties": {
            "operator": {
                "type": "string"
            },
            "arguments": {
                "type": "object"
            }
        }
    }
)


def get_object(integration, account_uuid, object_type, object_uuid, token, path_override=None, **kwargs):
    from urllib.parse import urljoin
    import requests
    results = {
        object_type: None,
        "exists": False
    }
    path = path_override if path_override is not None else f'/{object_type}s/{object_uuid}'
    resp = requests.get(urljoin(integration['base_url'], path), headers=token)
    if resp.status_code == 200:
        results['exists'] = True
        results[object_type] = resp.json()['response']
    return results


def create_object(integration, account_uuid, object_type, data, token, path_override=None, **kwargs):
    from urllib.parse import urljoin
    import requests
    results = {
        object_type: None,
        "created": False
    }
    path = path_override if path_override is not None else f'/{object_type}s/'
    resp = requests.post(urljoin(integration['base_url'], path), json=data, headers=token)
    if resp.status_code == 200:
        results['created'] = True
        results[object_type] = resp.json()['response']
    return results


def update_object(integration, account_uuid, object_type, object_uuid, data, token, path_override=None, **kwargs):
    from urllib.parse import urljoin
    import requests
    results = {
        object_type: None,
        "updated": False
    }
    path = path_override if path_override is not None else f'/{object_type}s/{object_uuid}'
    resp = requests.patch(urljoin(integration['base_url'], path), json=data, headers=token)
    if resp.status_code == 200:
        results['updated'] = True
        results[object_type] = resp.json()['response']
    return results


def search_objects(integration, search_parameters, plural_object_type, token, limit=100, **kwargs):
    objects = []
    search = True

    page = 1
    while search:
        payload = dict(
            limit=limit,
            search_parameters=search_parameters
        )
        if limit is not None:
            payload['page'] = page
        resp = requests.post(
            url=urljoin(integration['extra_attributes']['base_url'], f'/{plural_object_type}/search'),
            json=payload,
            headers=token
        )
        objects.extend(resp.json()['response'])
        if limit is None or len(resp.json()['response']) < limit:
            search = False
        page += 1
    return {plural_object_type: objects}


def trigger_object(inputs):
    return inputs['record']
