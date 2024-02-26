import re


def validate_email(email):
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    else:
        return False


def validate_date(year, month, day):
    try:
        year = int(year)
        month = int(month)
        day = int(day)
        if 1 <= month <= 12 and 1 <= day <= 31:
            return True
        else:
            return False
    except ValueError:
        return False


def validate_time(time):
    try:
        hours, minutes = map(int, time.split(':'))
        if 0 <= hours < 24 and 0 <= minutes < 60:
            return True
        else:
            return False
    except (ValueError, AttributeError):
        return False
