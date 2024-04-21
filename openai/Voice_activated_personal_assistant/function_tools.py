code_interpreter = {
    "type": "code_interpreter"
}


list_reminders_function = {
    "type": "function",
    "function": {
        "name": "list_reminders",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        },
        "description": "Lists all reminders stored in the reminders.txt file, formatted as a single string. runs before"
                       "each delete reminder function call to show the current reminders."
    }
}





remover_reminder_function = {
    "type": "function",
    "function": {
        "name": "remove_reminder",
        "parameters": {
            "type": "object",
            "properties": {
                "reminder_text": {
                    "type": "string",
                    "description": "The text of the reminder to remove."
                                   "runs after list_reminders to show the current reminders."
                }
            },
            "required": ["reminder_text"]
        }
    }
}

add_reminder_function = {
    "type": "function",
    "function": {
        "name": "add_reminder",
        "parameters": {
            "type": "object",
            "properties": {
                "reminder_text": {
                    "type": "string",
                    "description": "The text of the reminder to add."
                }
            },
            "required": ["reminder_text"]
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
