code_interpreter = {
    "type": "code_interpreter"
}

create_file_function = {
    "type": "function",
    "function": {
        "name": "create_text_file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_name": {
                    "type": "string",
                    "description": "The name of the file to be created, Dont create the file if i didnt use the word create file"
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

date_time_now_function = {
    "type": "function",
    "function": {
        "name": "date_time_now",
        "description": "This function returns the local current date and time information. dont be very specific, just use the needed information",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}

local_temperature_info = {
    "type": "function",
    "function": {
        "name": "local_temperature_info",
        "description": "This function returns the local forcast temperature information.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}
