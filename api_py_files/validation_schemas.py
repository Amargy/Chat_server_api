#!/usr/bin/env python3

validate_schema_for_new_user_request = {
    "additionalProperties": False,
    "type": "object",
    "properties": {
        "username": {"type": "string", "minLength": 1, "maxLength": 200}
    },
}

validate_schema_for_new_chat_request = {
    "additionalProperties": False,
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1, "maxLength": 200},
        "users": {"type": "array", "minItems": 2, "items": {"type": "string"}},
    },
}

validate_schema_for_new_message = {
    "additionalProperties": False,
    "type": "object",
    "properties": {
        "chat": {"type": "string", "minLength": 1, "maxLength": 200},
        "author": {"type": "string", "minLength": 1, "maxLength": 200},
        "text": {"type": "string", "minLength": 1, "maxLength": 200},
    },
}

validate_schema_for_get_chat_list = {
    "additionalProperties": False,
    "type": "object",
    "properties": {
        "user": {"type": "string", "minLength": 1, "maxLength": 200}
    },
}

validate_schema_for_get_message_list = {
    "additionalProperties": False,
    "type": "object",
    "properties": {
        "chat": {"type": "string", "minLength": 1, "maxLength": 200}
    },
}
