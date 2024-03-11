create_file_function = {
    "type": "function",
    "function": {
        "name": "create_text_file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_name": {
                    "type": "string",
                    "description": "The name of the file to be created"
                },
                "content": {
                    "type": "string",
                    "description": "The content to write inside the file. Defaults to an empty string if not provided."
                }
            },
            "required": ["file_name"]
        }
    }
}

delete_file_function = {
    "type": "function",
    "function": {
        "name": "delete_file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_name": {
                    "type": "string",
                    "description": "The name of the file to be deleted"
                }
            },
            "required": ["file_name"]
        }
    }
}

delete_all_txt_files_function = {
    "type": "function",
    "function": {
        "name": "delete_all_txt_files",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}

finish_conversation_function = {
    "type": "function",
    "function": {
        "name": "finish_conversation",
        "parameters": {
            "type": "object",
            "properties": {
                "value": {
                    "type": "boolean",
                    "description": "Weather to end the conversation or not."
                }
            },
            "required": ["value"]
        }
    }
}
