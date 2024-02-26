OBJECT_SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'required': ['account_uuid', 'name', 'nodes', 'edges', 'is_inherited'],
    'properties': {
        'account_uuid': {'type': 'string',
                         'format': '[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}'},
        'is_inherited': {'type': 'boolean'},
        'workflow_uuid': {'type': 'string',
                          'format': '[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}',
                          'readOnly': True},
        'trigger_integration_operation_keys': {'type': 'array', 'readOnly': True, 'items': {'type': 'string'}},
        'trigger_operation_uuids': {'type': 'array', 'readOnly': True, 'items': {'type': 'string',
                                                                                 'format': '[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}'}},
        'name': {'type': 'string'},
        'description': {'type': 'string', 'default': None, 'nullable': True},
        'nodes': {
            'type': 'array',
            'items': {
                'type': 'object', 'additionalProperties': False,
                'required': ['node_id', 'name', 'is_trigger', 'integration_uuid', 'operation_key', 'inputs'],
                'properties': {
                    'integration_uuid': {'type': 'string',
                                         'format': '[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}'},
                    'node_uuid': {'type': 'string',
                                  'format': '[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}',
                                  'readOnly': True}, 'node_id': {'type': 'integer'}, 'name': {'type': 'string'},
                    'is_trigger': {'type': 'boolean', 'default': False}, 'integration_key': {'type': 'string'},
                    'operation_key': {'type': 'string'}, 'operation_uuid': {'type': 'string',
                                                                            'format': '[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}',
                                                                            'readOnly': True},
                    'expand_keys': {'default': [], 'type': 'array',
                                    'items': {'type': 'object', 'properties': {'path': {'type': 'string'}}}},
                    'inputs': {'type': 'object'}}}},
        'edges': {
            'type': 'array',
            'items': {
                'type': 'object',
                'additionalProperties': False,
                'required': ['edge_id', 'source_id', 'target_id'],
                'properties': {
                    'edge_uuid': {'type': 'string',
                                  'format': '[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}',
                                  'readOnly': True},
                    'edge_id': {'type': 'integer'}, 'label': {'type': 'string'}, 'source_id': {'type': 'integer'},
                    'source_uuid': {'type': 'string',
                                    'format': '[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}',
                                    'readOnly': True},
                    'target_id': {'type': 'integer'},
                    'target_uuid': {'type': 'string',
                                    'format': '[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}',
                                    'readOnly': True},
                    'expand_keys': {'default': [], 'type': 'array',
                                    'items': {'type': 'object', 'properties': {'path': {'type': 'string'}}}},
                    'filters': {'oneOf': [
                        {'type': 'object', 'additionalProperties': False, 'required': ['operator', 'operations'],
                         'properties': {'operator': {'type': 'string', 'enum': ['and', 'or']},
                                        'operations': {'type': 'array', 'items': {'oneOf': [{'oneOf': [...]},
                                                                                            {'type': 'object',
                                                                                             'additionalProperties': False,
                                                                                             'required': ['left',
                                                                                                          'right',
                                                                                                          'operator'],
                                                                                             'properties': {'left': {
                                                                                                 'oneOf': [
                                                                                                     {'type': 'object',
                                                                                                      'additionalProperties': False,
                                                                                                      'required': [
                                                                                                          'value'],
                                                                                                      'properties': {
                                                                                                          'value': {
                                                                                                              'nullable': True,
                                                                                                              'anyOf': [
                                                                                                                  {
                                                                                                                      'type': 'string'},
                                                                                                                  {
                                                                                                                      'type': 'number'},
                                                                                                                  {
                                                                                                                      'type': 'boolean'},
                                                                                                                  {
                                                                                                                      'type': 'integer'}]},
                                                                                                          'transforms': {
                                                                                                              'type': 'array',
                                                                                                              'items': {
                                                                                                                  'type': 'object',
                                                                                                                  'additionalProperties': False,
                                                                                                                  'required': [
                                                                                                                      'operator',
                                                                                                                      'arguments'],
                                                                                                                  'properties': {
                                                                                                                      'operator': {
                                                                                                                          'type': 'string'},
                                                                                                                      'arguments': {
                                                                                                                          'type': 'object'}}}}}},
                                                                                                     {'type': 'object',
                                                                                                      'additionalProperties': False,
                                                                                                      'required': [
                                                                                                          'path'],
                                                                                                      'properties': {
                                                                                                          'path': {
                                                                                                              'type': 'string'},
                                                                                                          'default': {
                                                                                                              'nullable': True,
                                                                                                              'anyOf': [
                                                                                                                  {
                                                                                                                      'type': 'string'},
                                                                                                                  {
                                                                                                                      'type': 'number'},
                                                                                                                  {
                                                                                                                      'type': 'boolean'},
                                                                                                                  {
                                                                                                                      'type': 'integer'}]},
                                                                                                          'use_first_result': {
                                                                                                              'type': 'boolean',
                                                                                                              'default': True},
                                                                                                          'transforms': {
                                                                                                              'type': 'array',
                                                                                                              'items': {
                                                                                                                  'type': 'object',
                                                                                                                  'additionalProperties': False,
                                                                                                                  'required': [
                                                                                                                      'operator',
                                                                                                                      'arguments'],
                                                                                                                  'properties': {
                                                                                                                      'operator': {
                                                                                                                          'type': 'string'},
                                                                                                                      'arguments': {
                                                                                                                          'type': 'object'}}}}}}]},
                                                                                                            'operator': {
                                                                                                                'type': 'string',
                                                                                                                'enum': [
                                                                                                                    '>',
                                                                                                                    '<',
                                                                                                                    'contains',
                                                                                                                    '>=',
                                                                                                                    '==',
                                                                                                                    '!=',
                                                                                                                    '<=']},
                                                                                                            'right': {
                                                                                                                'oneOf': [
                                                                                                                    {
                                                                                                                        'type': 'object',
                                                                                                                        'additionalProperties': False,
                                                                                                                        'required': [
                                                                                                                            'value'],
                                                                                                                        'properties': {
                                                                                                                            'value': {
                                                                                                                                'nullable': True,
                                                                                                                                'anyOf': [
                                                                                                                                    {
                                                                                                                                        'type': 'string'},
                                                                                                                                    {
                                                                                                                                        'type': 'number'},
                                                                                                                                    {
                                                                                                                                        'type': 'boolean'},
                                                                                                                                    {
                                                                                                                                        'type': 'integer'}]},
                                                                                                                            'transforms': {
                                                                                                                                'type': 'array',
                                                                                                                                'items': {
                                                                                                                                    'type': 'object',
                                                                                                                                    'additionalProperties': False,
                                                                                                                                    'required': [
                                                                                                                                        'operator',
                                                                                                                                        'arguments'],
                                                                                                                                    'properties': {
                                                                                                                                        'operator': {
                                                                                                                                            'type': 'string'},
                                                                                                                                        'arguments': {
                                                                                                                                            'type': 'object'}}}}}},
                                                                                                                    {
                                                                                                                        'type': 'object',
                                                                                                                        'additionalProperties': False,
                                                                                                                        'required': [
                                                                                                                            'path'],
                                                                                                                        'properties': {
                                                                                                                            'path': {
                                                                                                                                'type': 'string'},
                                                                                                                            'default': {
                                                                                                                                'nullable': True,
                                                                                                                                'anyOf': [
                                                                                                                                    {
                                                                                                                                        'type': 'string'},
                                                                                                                                    {
                                                                                                                                        'type': 'number'},
                                                                                                                                    {
                                                                                                                                        'type': 'boolean'},
                                                                                                                                    {
                                                                                                                                        'type': 'integer'}]},
                                                                                                                            'use_first_result': {
                                                                                                                                'type': 'boolean',
                                                                                                                                'default': True},
                                                                                                                            'transforms': {
                                                                                                                                'type': 'array',
                                                                                                                                'items': {
                                                                                                                                    'type': 'object',
                                                                                                                                    'additionalProperties': False,
                                                                                                                                    'required': [
                                                                                                                                        'operator',
                                                                                                                                        'arguments'],
                                                                                                                                    'properties': {
                                                                                                                                        'operator': {
                                                                                                                                            'type': 'string'},
                                                                                                                                        'arguments': {
                                                                                                                                            'type': 'object'}}}}}}]}}}]}}}},
                        {'type': 'object', 'additionalProperties': False, 'required': ['operator', 'operations'],
                         'properties': {'operator': {'type': 'string', 'enum': ['not']},
                                        'operations': {'type': 'array', 'minItems': 1, 'maxItems': 1, 'items': {
                                            'oneOf': [{'oneOf': [...]},
                                                      {'type': 'object', 'additionalProperties': False,
                                                       'required': ['left', 'right', 'operator'], 'properties': {
                                                          'left': {'oneOf': [
                                                              {'type': 'object', 'additionalProperties': False,
                                                               'required': ['value'], 'properties': {
                                                                  'value': {'nullable': True,
                                                                            'anyOf': [{'type': 'string'},
                                                                                      {'type': 'number'},
                                                                                      {'type': 'boolean'},
                                                                                      {'type': 'integer'}]},
                                                                  'transforms': {'type': 'array',
                                                                                 'items': {'type': 'object',
                                                                                           'additionalProperties': False,
                                                                                           'required': ['operator',
                                                                                                        'arguments'],
                                                                                           'properties': {'operator': {
                                                                                               'type': 'string'},
                                                                                                          'arguments': {
                                                                                                              'type': 'object'}}}}}},
                                                              {'type': 'object', 'additionalProperties': False,
                                                               'required': ['path'],
                                                               'properties': {'path': {'type': 'string'},
                                                                              'default': {'nullable': True,
                                                                                          'anyOf': [{'type': 'string'},
                                                                                                    {'type': 'number'},
                                                                                                    {'type': 'boolean'},
                                                                                                    {
                                                                                                        'type': 'integer'}]},
                                                                              'use_first_result': {'type': 'boolean',
                                                                                                   'default': True},
                                                                              'transforms': {'type': 'array',
                                                                                             'items': {'type': 'object',
                                                                                                       'additionalProperties': False,
                                                                                                       'required': [
                                                                                                           'operator',
                                                                                                           'arguments'],
                                                                                                       'properties': {
                                                                                                           'operator': {
                                                                                                               'type': 'string'},
                                                                                                           'arguments': {
                                                                                                               'type': 'object'}}}}}}]},
                                                          'operator': {'type': 'string',
                                                                       'enum': ['>', '<', 'contains', '>=', '==', '!=',
                                                                                '<=']}, 'right': {'oneOf': [
                                                              {'type': 'object', 'additionalProperties': False,
                                                               'required': ['value'], 'properties': {
                                                                  'value': {'nullable': True,
                                                                            'anyOf': [{'type': 'string'},
                                                                                      {'type': 'number'},
                                                                                      {'type': 'boolean'},
                                                                                      {'type': 'integer'}]},
                                                                  'transforms': {'type': 'array',
                                                                                 'items': {'type': 'object',
                                                                                           'additionalProperties': False,
                                                                                           'required': ['operator',
                                                                                                        'arguments'],
                                                                                           'properties': {'operator': {
                                                                                               'type': 'string'},
                                                                                                          'arguments': {
                                                                                                              'type': 'object'}}}}}},
                                                              {'type': 'object', 'additionalProperties': False,
                                                               'required': ['path'],
                                                               'properties': {'path': {'type': 'string'},
                                                                              'default': {'nullable': True,
                                                                                          'anyOf': [{'type': 'string'},
                                                                                                    {'type': 'number'},
                                                                                                    {'type': 'boolean'},
                                                                                                    {
                                                                                                        'type': 'integer'}]},
                                                                              'use_first_result': {'type': 'boolean',
                                                                                                   'default': True},
                                                                              'transforms': {'type': 'array',
                                                                                             'items': {'type': 'object',
                                                                                                       'additionalProperties': False,
                                                                                                       'required': [
                                                                                                           'operator',
                                                                                                           'arguments'],
                                                                                                       'properties': {
                                                                                                           'operator': {
                                                                                                               'type': 'string'},
                                                                                                           'arguments': {
                                                                                                               'type': 'object'}}}}}}]}}}]}}}}]}}}},
        'created_by_user_uuid': {'type': 'string',
                                 'format': '[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}',
                                 'readOnly': True},
        'updated_by_user_uuid': {'type': 'string',
                                 'format': '[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}',
                                 'readOnly': True},
        'created_ts': {'type': 'integer', 'readOnly': True},
        'updated_ts': {'type': 'integer', 'readOnly': True},
        'status_id': {'type': 'integer', 'default': 1},
        'status_name': {'type': 'string', 'readOnly': True},
        'is_active': {'default': True, 'readOnly': True},
        'is_visible': {'default': True, 'readOnly': True}
    }
}
