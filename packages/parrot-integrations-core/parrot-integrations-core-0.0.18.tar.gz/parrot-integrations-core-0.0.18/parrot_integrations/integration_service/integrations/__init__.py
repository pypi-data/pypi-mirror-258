OBJECT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "name",
        "integration_type_uuid",
        "account_uuid",
        "extra_attributes"
    ],
    "properties": {
        "account_uuid": {
            "type": "string",
            "format": "[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}"
        },
        "integration_uuid": {
            "type": "string",
            "format": "[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}",
            "readOnly": True
        },
        "integration_type_uuid": {
            "type": "string",
            "format": "[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}"
        },
        "integration_key": {
            "type": "string"
        },
        "name": {
            "type": "string"
        },
        "is_default_integration": {
            "type": "boolean",
            "default": False,
            "writeOnly": True
        },
        "extra_attributes": {
            "type": "object"
        },
        "credentials": {
            "type": "object",
            "writeOnly": True
        },
        "encrypted_credentials": {
            "type": "string"
        },
        "external_attributes": {
            "type": "object",
            "readOnly": True
        },
        "status_id": {
            "type": "integer",
            "default": 1
        },
        "status_name": {
            "type": "string",
            "readOnly": True
        },
        "status_description": {
            "type": "string",
            "readOnly": True
        },
        "is_active": {
            "type": "boolean",
            "readOnly": True
        },
        "is_visible": {
            "type": "boolean",
            "readOnly": True
        },
        "created_ts": {
            "type": "integer",
            "readOnly": True
        },
        "updated_ts": {
            "type": "integer",
            "readOnly": True
        }
    }
}
