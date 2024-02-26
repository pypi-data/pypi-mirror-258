import pathlib
import sys


sys.path.append(pathlib.Path.cwd().as_posix())


from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta, date


from utils import config
from utils import auth
from utils.check_input_error import *


def create_event(creds, start_time, end_time, description, booker_email):
    service = build("calendar", "v3", credentials=creds)
    event = {
        "summary": description,
        "start": {"dateTime": start_time, "timeZone": "Africa/Johannesburg"},
        "end": {"dateTime": end_time, "timeZone": "Africa/Johannesburg"},
        "attendees": [{"email": booker_email}],
    }
    try:
        event = (
            service.events().insert(calendarId=config.CALENDAR_ID, body=event).execute()
        )
        print(f"Booked slot from {start_time} to {end_time} for {booker_email}")
    except HttpError as error:
        print(f"An error occurred: {error}")


def is_slot_available(creds, start_time, end_time):
    """
    Check if a slot on the specified calendar is available.
    """
    service = build("calendar", "v3", credentials=creds)
    events_result = (
        service.events()
        .list(
            calendarId=config.CALENDAR_ID,
            timeMin=start_time,
            timeMax=end_time,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])
    return not bool(events)


def is_working_day(year, month, day):
    """
    Check if the specified date is a working day (Monday to Friday).
    """
    selected_date = date(int(year), int(month), int(day))
    return selected_date.weekday() < 5  


def book_slot(creds, year, month, day, time, description, booker_email):
    if not is_working_day(year, month, day):
        print("Booking can only be made for working days (Monday to Friday).")
        return

    if not validate_date(year, month, day):
        print("Invalid date. Please enter a valid date.")
        return None

    
    if not booker_email.endswith(("@student.wethinkcode.co.za", "@wethinkcode.co.za")):
        print("Invalid email. Booking can only be made with a wethinkcode.co.za email.")
        return

    now = datetime.utcnow()
    time = datetime.strptime(time, "%H:%M")
    start_time_obj = datetime.combine(
        date(int(year), int(month), int(day)), time.time()
    )

    end_time_obj = start_time_obj + timedelta(minutes=30)

    if start_time_obj < now:
        print("Cannot book a past date.")
        return

    if not (8 <= start_time_obj.hour < 16):
        print("Booking can only be made between 08:00 and 16:00.")
        return

    start_time_formatted = start_time_obj.isoformat() + "Z"
    end_time_formatted = end_time_obj.isoformat() + "Z"

    if is_slot_available(creds, start_time_formatted, end_time_formatted):
        create_event(
            creds, start_time_formatted, end_time_formatted, description, booker_email
        )
    else:
        print("This slot is already booked.")


def get_inputs():
    booker_email = input("Enter your email: ")
    year = input("Enter the year for the slot: ")
    month = input("Enter the month for the slot: ")
    day = input("Enter the day for the slot: ")
    time = input("Enter the time for the slot (24-hour format): ")
    description = input("Enter the description for the booking: ")

    if not validate_date(year, month, day):
        print("Invalid date. Please enter a valid date.")
        return None

    if not validate_time(time):
        print("Invalid time. Please enter time in 24-hour format (HH:MM).")
        return None

    if not validate_email(booker_email):
        print("Invalid email. Please enter a valid email.")
        return None

    return year, month, day, time, description, booker_email


def volunteer_assistance(creds):
    year, month, day, time, description, booker_email = get_inputs()
    book_slot(creds, year, month, day, time, description, booker_email)


if __name__ == "__main__":
    creds = auth.authenticate()
    volunteer_assistance(creds)

