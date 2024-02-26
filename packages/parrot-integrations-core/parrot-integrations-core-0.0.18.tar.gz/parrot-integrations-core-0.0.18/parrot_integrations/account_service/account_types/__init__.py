OBJECT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "name",
        "schema",
        "description",
        "account_uuid"
    ],
    "properties": {
        "account_type_uuid": {
            "type": "string",
            "format": "[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}",
            "readOnly": True
        },
        "account_uuid": {
            "type": "string",
            "format": "[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}"
        },
        "name": {
            "type": "string"
        },
        "description": {
            "type": "string"
        },
        "schema": {
            "type": "object"
        },
        "is_inherited": {
            "type": "boolean",
            "default": False
        },
        "status_id": {
            "type": "integer",
            "default": 1
        },
        "status_name": {
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
