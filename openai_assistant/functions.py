import os
import datetime
import json
import pytz

from api_requests import local_time_and_air_temperature

def add_reminder(reminder_text):
    """Add a reminder to the reminders.txt file."""
    with open("reminders.txt", "a") as file:
        file.write(reminder_text + "\n")


def remove_reminder(reminder_text):
    """Remove a reminder from the reminders.txt file."""
    with open("reminders.txt", "r") as file:
        lines = file.readlines()

    with open("reminders.txt", "w") as file:
        for line in lines:
            if line.strip("\n") != reminder_text:
                file.write(line)


def list_reminders():
    """List all reminders in the reminders.txt file."""
    with open("reminders.txt", "r") as file:
        reminders = file.readlines()

    return str(reminders)


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

    # print(json_string)

    return json_string


def local_temperature_info():
    current_time_info = date_time_now()
    forcast_data = local_time_and_air_temperature()

    my_location_weather_wather_info = {
        "current_time_info": current_time_info,
        "forcast_data": forcast_data
    }

    # print(my_location_weather_wather_info)

    return my_location_weather_wather_info

if __name__ == "__main__":
    # Test the functions
    l = list_reminders()
    print(l)
    print(type(l))
    pass