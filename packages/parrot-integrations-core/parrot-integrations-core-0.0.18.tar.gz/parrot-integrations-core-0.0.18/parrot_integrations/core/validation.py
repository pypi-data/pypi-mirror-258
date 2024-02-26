import inspect
from copy import deepcopy
from importlib import reload

from parrot_integrations.core.common import load_integration_module


def validate_integration(integration_key):
    integration = load_integration_module(integration_key=integration_key)
    assert hasattr(integration, 'get_integration_schema')
    assert hasattr(integration, 'connect')
    schema_signature = inspect.signature(integration.get_integration_schema)
    connect_signature = inspect.signature(integration.connect)
    assert len(schema_signature.parameters.keys()) == 0
    assert len(connect_signature.parameters.keys()) == 2
    assert 'extra_attributes' in connect_signature.parameters.keys()
    assert 'credentials' in connect_signature.parameters.keys()
    assert integration.get_integration_schema()


def validate_operation(integration_key, operation_key):
    from parrot_integrations.core.schemas import get_operation_schema
    operation = load_integration_module(integration_key=integration_key, operation_key=operation_key)
    object_schema = None
    if hasattr(operation, 'OBJECT_SCHEMA'):
        object_schema = deepcopy(operation.OBJECT_SCHEMA)
    assert hasattr(operation, 'get_schema')
    assert hasattr(operation, 'process')
    schema_signature = inspect.signature(operation.get_schema)
    process_signature = inspect.signature(operation.process)
    assert len(schema_signature.parameters.keys()) == 0
    schema = operation.get_schema()
    operation_schema = get_operation_schema(integration_key=integration_key, operation_key=operation_key)
    validate_input_schema(inputs=operation_schema['schema']['properties']['inputs'])
    if hasattr(operation, 'OBJECT_SCHEMA'):
        reload(operation)
        assert operation.OBJECT_SCHEMA == object_schema
    assert operation_schema['schema']['type'] == 'object'
    assert operation_schema['schema']['properties']['outputs']
    assert not operation_schema['schema']['additionalProperties']
    kwarg_parameter = any(i.kind.name == 'VAR_KEYWORD' for i in process_signature.parameters.values())
    for keyword in ['workflow_uuid', 'node_uuid', 'processed_ts', 'inputs', 'integration']:
        assert keyword in process_signature.parameters.keys() or kwarg_parameter


def validate_input_schema(inputs):
    print(inputs)
    for i in inputs.get('required', []):
        assert i in inputs['properties'].keys()
    if inputs.get('type') == 'object':
        for k, v in inputs.get('properties', dict()).items():
            print(k, v)
            if v.get('type') == 'object':
                validate_input_schema(inputs=v)
            elif v.get('type') == 'array':
                validate_input_schema(inputs=v['items'])
            elif inputs.get('type'):
                assert isinstance(inputs['type'], str) or isinstance(inputs['type'], list)
            else:
                assert 'oneOf' in v.keys()
    elif inputs.get('type') == 'array':
        validate_input_schema(inputs=inputs['items'])
    elif inputs.get('type'):
        assert isinstance(inputs['type'], str) or isinstance(inputs['type'], list)
    else:
        assert len(inputs['oneOf']) >= 1
        for i in inputs['oneOf']:
            validate_input_schema(inputs=i)
