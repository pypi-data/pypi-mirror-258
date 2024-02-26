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
        "context_type_uuid": {
            "type": "string",
            "format": "[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}",
            "readOnly": True
        },
        "account_uuid": {
            "type": "string",
            "format": "[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}"
        },
        "content_type": {
            "type": "string",
            "default": "string",
            "enum": [
                "file",
                "string"
            ]
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
        "is_encrypted": {
            "type": "boolean",
            "default": False
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
