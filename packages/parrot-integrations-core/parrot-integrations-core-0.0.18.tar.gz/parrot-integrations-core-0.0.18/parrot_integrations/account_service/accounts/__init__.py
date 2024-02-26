OBJECT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "name",
        "account_type_uuid",
        "extra_attributes"
    ],
    "properties": {
        "parent_account_uuids": {
            "type": "array",
            "uniqueItems": True,
            "items": {
                "type": "string",
                "format": "[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}"
            }
        },
        "account_uuid": {
            "type": "string",
            "format": "[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}",
            "readOnly": True
        },
        "account_type_uuid": {
            "type": "string",
            "format": "[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}"
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
        }
    }
}
