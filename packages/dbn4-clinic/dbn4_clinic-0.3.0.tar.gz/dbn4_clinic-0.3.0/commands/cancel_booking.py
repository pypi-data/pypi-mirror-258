import pathlib
import json
import sys


sys.path.append(pathlib.Path.cwd().as_posix())


from googleapiclient.discovery import build


from utils import config
from utils import auth
from commands.view_calendar import *


SCOPES = ["https://www.googleapis.com/auth/calendar"]

calendar_data = config.FILENAMES["calendar_data"]


def cancel_booking(student_email, slot_date, slot_time):
    """
    Cancels an attendee if available and updates the data file with the booking information.
    - data_file: The path to the JSON file containing slot data.
    """
    creds = auth.authenticate()
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
            if date == slot_date and start_time[0:5] == slot_time:
                event_ID = event_data.get("id")
                break  
                # # Exit the loop once a matching slot is foit diffund   
    if event_ID is None:
        print("Slot not found or does not exist.")
        return    
    calendar_Id = config.CALENDAR_ID    
    event = service.events().get(calendarId=calendar_Id, eventId=event_ID).execute()
    
    if 'attendees' in event: 
        if event['attendees']['email'] != student_email:
            print('The event you are trying to cancel is not yours.')
            return
        else:
            event['attendees'].remove()
            updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()      
            print("Event deleted successfully.")
    if is_update_needed(calendar_data):
        update_calendar_data(event)
  
            
        
def inputs():
    student_email = input("Enter your email: ")
    slot_date = input("Enter the date for the slot (YYYY-MM-DD): ")
    slot_time = input("Enter the start time for the slot (HH:MM): ")
    return student_email, slot_date, slot_time


if __name__ == "__main__":
    student_email, slot_date, slot_time = inputs()
    cancel_booking(student_email, slot_date, slot_time)
  


