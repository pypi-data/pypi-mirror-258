import datetime as dt
import os.path
import pathlib
import json
import sys


sys.path.append(pathlib.Path.cwd().as_posix())

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from prettytable import PrettyTable


from utils import auth
from utils import config


credentials_filename = config.FILENAMES["credentials"]
token_filename = config.FILENAMES["token"]


file_path = os.path.expanduser("~")
student_calendar = os.path.join(file_path, "student_calendar.json")


def code_clinic_file(calendar_data):
    if not os.path.exists(calendar_data):
        with open(calendar_data, "w") as file:
            file.write(json.dumps({}))


def code_student_file():
    if not os.path.exists(student_calendar):
        with open(student_calendar, "w") as file:
            file.write(json.dumps({}))
    return student_calendar


def get_code_clinic_calendar_events(creds):

    try:
        service = build("calendar", "v3", credentials=creds)
        now = dt.datetime.utcnow().isoformat() + "Z"
        next_days = (dt.datetime.utcnow() + dt.timedelta(days=7)).isoformat() + "Z"
        event_request = (
            service.events()
            .list(
                calendarId=config.CALENDAR_ID,
                timeMin=now,
                timeMax=next_days,
                maxResults=7,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = event_request.get("items", [])

    except HttpError as error:
        print("An error occurred:", error)

    return events


def update_calendar_data(events, calendar_data):
    try:
        with open(calendar_data, "r") as file:
            stored_data = json.load(file)
    except FileNotFoundError:
        stored_data = {}
    
    day = dt.datetime.now().date()
  
    stored_data = {
        start: event_data
        for start, event_data in stored_data.items()
        if dt.datetime.strptime(start.split("T")[0], "%Y-%m-%d").date() >= day
    }
    
    for event in events:
        try:
       
            start = event["start"].get("dateTime", event["start"].get("date"))
            end = event["end"].get("dateTime", event["end"].get("date"))
            summary = event["summary"]
            event_ID = event["id"]
            creator = event.get("creator", {}).get("email", "")
            attendee = event.get("attendee", {}).get("email", "")
            description = event.get("description", "No description provided")

            stored_data[start] = {
                "summary": summary,
                "creator": creator,
                "attendee": attendee,
                "description": description,
                "end": end,
                "id": event_ID,
            }
        except KeyError as e:
            print(f"KeyError: {e} occurred in the following event:")

    with open(calendar_data, "w") as file:
        json.dump(stored_data, file)


def is_update_needed(calendar_data_file):
    try:
        with open(calendar_data_file, "r") as file:
            stored_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return True
    today = dt.datetime.now().date()
    seven_days_from_now = today + dt.timedelta(days=7)
    stored_event_dates = [
        dt.datetime.strptime(event.split("T")[0], "%Y-%m-%d").date()
        for event in stored_data.keys()
    ]
    for single_date in (today + dt.timedelta(n) for n in range(7)):
        if single_date not in stored_event_dates and single_date <= seven_days_from_now:
            return True
    return False


def print_code_clinic_calendar(calendar_data):
    """Check if "T" is in the start string
    Split the datetime string into date and start time
    """

    try:
        with open(calendar_data, "r") as file:
            stored_data = json.load(file)
    except FileNotFoundError:
        stored_data = {}
        
    events_output = PrettyTable()
    events_output.field_names = (
        "Event_Id",
        "Date",
        "Start Time",
        "End Time",
        "Topic",
        "Vounteer",
        "Description",
        "Status",
    )

    if not stored_data:
        print("No upcoming events found")
        return

    print("Upcoming events.")

    today = dt.datetime.now().date()
    for start, event_data in stored_data.items():
        event_date = dt.datetime.strptime(start.split("T")[0], "%Y-%m-%d").date()
        if today <= event_date <= (today + dt.timedelta(days=7)):
            if "T" in start:
                date, start_time = start.split("T")
            else:
                date = start
                start_time = ""
            end = event_data["end"]
            if "T" in end:
                _, end_time = end.split("T")
            else:
                end_time = ""
            event_ID = event_data["id"]
            summary = event_data["summary"]
            creator = event_data["creator"]
            attendee = event_data["attendee"]
            description = event_data["description"]
            status = "Booked" if attendee != "" else "Available"

            events_output.add_row(
                [
                    event_ID,
                    date,
                    start_time[0:5],
                    end_time[0:5],
                    summary,
                    creator,
                    description,
                    status,
                ]
            )
   
    print(events_output)


def get_student_calendar_events(creds):

    try:
        service = build("calendar", "v3", credentials=creds)
        now = dt.datetime.now().isoformat() + "Z"

        event_request = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=7,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = event_request.get("items", [])

    except HttpError as error:
        print("An error occurred:", error)
    return events


def update_student_calendar(events):
    try:
        with open(student_calendar, "r") as file:
            student_data = json.load(file)
    except FileNotFoundError:
        student_data = {}

    day = dt.datetime.now().date()

    student_data = {
        start: event_data
        for start, event_data in student_data.items()
        if dt.datetime.strptime(start.split("T")[0], "%Y-%m-%d").date() >= day
    }

    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        end = event["end"].get("dateTime", event["end"].get("date"))
        summary = event["summary"]
        event_ID = event["id"]
        creator = event.get("creator", {}).get("email", "")
        attendee = event.get("attendee", {}).get("email", "")
        description = event.get("description", "No description provided")
        student_data[start] = {
            "summary": summary,
            "creator": creator,
            "attendee": attendee,
            "description": description,
            "end": end,
            "id": event_ID,
        }

    with open(student_calendar, "w") as file:
        json.dump(student_data, file)


def is_student_update_needed(student_calendar):
    try:
        with open(student_calendar, "r") as file:
            student_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return True
    today = dt.datetime.now().date()
    seven_days_from_now = today + dt.timedelta(days=7)
    stored_event_dates = [
        dt.datetime.strptime(event.split("T")[0], "%Y-%m-%d").date()
        for event in student_data.keys()
    ]
    for single_date in (today + dt.timedelta(n) for n in range(7)):
        if single_date not in stored_event_dates and single_date <= seven_days_from_now:
            return True
    return False


def print_student_calendar():
    try:
        with open(student_calendar, "r") as file:
            student_data = json.load(file)
    except FileNotFoundError:
        student_data = {}
    events_output = PrettyTable()

    events_output = PrettyTable()
    events_output.field_names = (
        "Date",
        "Start Time",
        "End Time",
        "Description",
    )

    if not student_data:
        print("No upcoming events found")
        return

    today = dt.datetime.now().date()
    for start, event_data in student_data.items():
        event_date = dt.datetime.strptime(start.split("T")[0], "%Y-%m-%d").date()
        if today <= event_date <= (today + dt.timedelta(days=7)):
            if "T" in start:
                date, start_time = start.split("T")
            else:
                date = start
                start_time = ""
            end = event_data["end"]
            if "T" in end:
                _, end_time = end.split("T")
            else:
                end_time = ""
            summary = event_data["summary"]
            events_output.add_row([date, start_time[0:5], end_time[0:5], summary])
            
    print(events_output)


def view_student_calendar(creds):
    """calls the functions to print the student calendar"""
    code_student_file()
    events = get_student_calendar_events(creds)
    is_student_update_needed(student_calendar)
    update_student_calendar(events)
    print_student_calendar()


def view_code_clinic_calendar(creds):
    calendar_data = config.FILENAMES["calendar_data"]
    code_clinic_file(calendar_data)
    events = get_code_clinic_calendar_events(creds)
    is_update_needed(calendar_data)
    update_calendar_data(events, calendar_data)
    print_code_clinic_calendar(calendar_data)


if __name__ == "__main__":

    config.create_working_directories()
    creds = auth.authenticate()

    calendar_type = input(
        "What calendar do you want to view student or code clinic: "
    ).lower()

    if calendar_type == "student":
        view_student_calendar(creds)

    elif calendar_type == "code clinic":
        view_code_clinic_calendar(creds)
    else:
        print("incorrect calendar chose")