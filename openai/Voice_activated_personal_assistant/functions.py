import os
import datetime
import json
import pytz



def create_text_file(file_name, content=""):
    try:
        with open(file_name, 'x') as file:
            file.write(content)
        return "file created successfully."
    except Exception as e:
        return f"An error occurred: {e}"


def delete_file(file_name):
    try:
        if os.path.exists(file_name):
            os.remove(file_name)
            return f"File '{file_name}' has been deleted."
        else:
            return f"File '{file_name}' does not exist."
    except Exception as e:
        return f"An error occurred: {e}"


def delete_all_txt_files():
    try:
        for file_name in os.listdir():
            if file_name.endswith('.txt'):
                os.remove(file_name)
                print(f"File '{file_name}' has been deleted.")
        return "All txt files have been deleted."
    except Exception as e:
        return f"An error occurred: {e}"


def finish_conversation(value=False):
    return not value


def date_time_now():

    # Define Norway's timezone
    norway_timezone = pytz.timezone('Europe/Oslo')

    # Get the current date and time
    now = datetime.datetime.now(norway_timezone)

    # Prepare date and time information
    date_info = {
        "Current Date and Time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "Year": now.year,
        "Month": now.month,
        "Day of the Month": now.day,
        "Hour": now.hour,
        "Minute": now.minute,
        "Second": now.second,
        "Microsecond": now.microsecond,
        "Day of the Week (index)": now.weekday(),  # Monday is 0, Sunday is 6
        "Day of the Week (name)": now.strftime("%A"),  # Full weekday name
        "ISO Day of the Week": now.isoweekday(),  # Monday is 1, Sunday is 7
        "Week Number of the Year (ISO)": now.isocalendar()[1],  # ISO week number
        "ISO Year": now.isocalendar()[0],
        "ISO Weekday": now.isocalendar()[2]  # ISO weekday
    }

    # Convert to JSON string
    json_string = json.dumps(date_info, indent=4)

    print(json_string)

    return json_string
