OBJECT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "name",
        "account_uuid",
        "context_type_uuid",
        "extra_attributes"
    ],
    "properties": {
        "account_uuid": {
            "type": "string",
            "format": "[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}"
        },
        "context_uuid": {
            "type": "string",
            "format": "[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}",
            "readOnly": True
        },
        "context_type_uuid": {
            "type": "string",
            "format": "[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}"
        },
        "urls": {
            "readOnly": True,
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "content": {
            "type": "string"
        },
        "name": {
            "type": "string"
        },
        "extra_attributes": {
            "type": "object"
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
        },
        "version_id": {
            "type": "integer",
            "default": 1,
            "readOnly": True
        },
        "version_uuid": {
            "type": "string",
            "readOnly": True,
            "format": "[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}"
        },
        "created_by_user_uuid": {
            "type": "string",
            "readOnly": True,
            "nullable": True,
            "format": "[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}"
        },
        "updated_by_user_uuid": {
            "type": "string",
            "readOnly": True,
            "nullable": True,
            "format": "[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}"
        }
    }
}
