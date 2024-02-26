import pathlib
import sys


sys.path.append(pathlib.Path.cwd().as_posix())


from googleapiclient.discovery import build
import json


from utils import config
from utils import auth
from utils.check_input_error import *


calendar_data = config.FILENAMES["calendar_data"]


def book_slot(creds, student_email, slot_date, slot_time, description):
    """
    Books a volunteer slot if available and updates the data file with the booking information.

    - data_file: The path to the JSON file containing slot data.
    """

    service = build("calendar", "v3", credentials=creds)

    event_ID = None  # Initialize event_ID outside the loop

    try:
        with open(calendar_data, 'r') as file:
            stored_data = json.load(file)
    except FileNotFoundError:
        stored_data = {}

    for start, event_data in stored_data.items():
        if "T" in start:  # Check if "T" is in the start string
            date, start_time = start.split("T")
            if date == slot_date and start_time[:5] == slot_time:
                event_ID = event_data.get("id")
                break  # Exit the loop once a matching slot is foit diffund
    
    if event_ID is None:
        print("Slot not found or already booked.")
        return

    calendar_Id = config.CALENDAR_ID

    event = service.events().get(calendarId=calendar_Id, eventId=event_ID).execute()
    event['attendees'] = [{"email": student_email}]
    event['description'] = description
    updated_event = service.events().update(calendarId=calendar_Id, eventId=event_ID, body=event).execute()

    print(f"Successfully booked {updated_event['updated']}")


def inputs():
    student_email = input("Enter your email: ")
    while not validate_email(student_email):
        print("Invalid email. Please try again.")
        student_email = input("Enter your email: ")

    slot_date = input("Enter the date for the slot (YYYY-MM-DD): ")
    try:
        year, month, day = map(int, slot_date.split('-'))
        while not validate_date(year, month, day):
            print("Invalid date. Please try again.")
            slot_date = input("Enter the date for the slot (YYYY-MM-DD): ")
            year, month, day = map(int, slot_date.split('-'))
    except ValueError:
        print("Date format should be YYYY-MM-DD.")
        return None  # Or ask for the date again in a loop

    slot_time = input("Enter the start time for the slot (HH:MM): ")
    while not validate_time(slot_time):
        print("Invalid time. Please try again.")
        slot_time = input("Enter the start time for the slot (HH:MM): ")
        
    description = input("Enter the description for the help needed: ")
    return student_email, slot_date, slot_time, description
    

def book(creds):
    student_email, slot_date, slot_time, description = inputs()
    book_slot(creds, student_email, slot_date, slot_time, description)


if __name__ == "__main__":
    creds = auth.authenticate()
    book(creds)
