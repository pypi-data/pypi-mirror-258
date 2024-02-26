from commands import view_code_clinic_calendar
from commands import view_student_calendar

from commands import volunteer_assistance
from commands import book

from utils.auth import is_connected
from utils.config import display_info

from commands import cmd_cancel_assistance_session
from commands import cmd_cancel_volunteer_session
from commands import cmd_invalid
from commands import cmd_exit



def display_options():
    print("\nAvailable Commands\n")
    print(get_description())


def get_options():
    return {**get_options_taking_args(), **get_options_not_taking_args()}


def get_options_taking_args():
    return {
        "1": {
            "option": "View Clinic Calendar",
            "description": "View current Code Clinic bookings",
            "function": view_code_clinic_calendar,
        },
        "2": {
            "option": "View Personal Calendar",
            "description": "View all current bookings",
            "function": view_student_calendar,
        },
        "3": {
            "option": "Book Assistance",
            "description": "Book a 30min Session",
            "function": book,
        },
        "4": {
            "option": "Volunteer Assistance",
            "description": "Volunteer 30min of assistance",
            "function": volunteer_assistance,
        },
        "5": {
            "option": "Cancel Assistance Session",
            "description": "Cancel a booking",
            "function": cmd_cancel_assistance_session,
        },
        "6": {
            "option": "Cancel Volunteer Session",
            "description": "Cancel a volunteering session",
            "function": cmd_cancel_volunteer_session,
        },
        "7": {
            "option": "Validate Connection",
            "description": "Ensure successful connection to Google Calendar",
            "function": is_connected,
        },
    }


def get_options_not_taking_args():
    return {
        "8": {
            "option": "Configure",
            "description": "Provide/Update Programm Configurations",
            "function": display_info,
        },
        "9": {
            "option": "Exit",
            "description": "Ends the Code Clinic bookings program",
            "function": cmd_exit,
        },
    }


def get_longest_length_of_options(options_dict):
    """
    Determine the length of the longest `option` value
    in provided dict

    Parameter
    ---------
    options_dict : dict[dict]
        mapping of UI input integer to function and
        its related UI descriptors

    Return
    ------
    int
        length of the option in provided dict
    """

    return max(len(cmd_descript["option"]) for cmd_descript in options_dict.values())


def get_description():
    """
    Provides a formatted string representation of
    available options

    Return
    ------
    str
        formatted string representation of available
        options
    """

    options_dict = get_options()
    longest = get_longest_length_of_options(options_dict)

    description = ""

    for index, cmd_descript in options_dict.items():
        cmd, descript, *_ = cmd_descript.values()
        description += f"   [{index}]  {cmd.ljust(longest)}\t\t{descript}\n"

    return description


def execute(option, creds):
    """
    Executor of executor pattern wherein user provided
    options is executed as per available commands

    Parameter
    ---------
    option : str::digit
        digit representing selection from UI

    creds : Credentials
        credentials to google api

    Return
    ------
    None
    """

    selection = get_options_taking_args().get(option)

    if selection:
        func = selection.get("function")
        func(creds)
    elif option in "89":
        selection = get_options_not_taking_args().get(option)
        func = selection.get("function")
        func()
    else:
        cmd_invalid(option)

    print("\n" * 5)
