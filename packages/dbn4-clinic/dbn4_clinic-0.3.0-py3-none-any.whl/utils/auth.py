"""
Authentication module for project, ensures that the user's
credentials and token exit and have been validated. In
cases where there are no credentials, please see the REAME.

Where no token is present, a new one is created, assuming
that the credentials are authentic.
"""

import pathlib
import sys
import os


from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


sys.path.append(pathlib.Path.cwd().as_posix())


from utils import config


def is_connected(creds):
    """
    Ensures that the session is connected to googleapis
    althewhile having valid credentials

    Parameters
    ----------
    creds : Credentials
        credentials to google api

    Return
    ------
    bool
        True if connected else False
    """

    try:
        creds.refresh(Request())
        print("... and we are connected :)")
    except Exception:
        print(";( hmmm ... seems we can't talk to the calendars")
        return False
    return True


def load_creds_from_file(token_path, scopes):
    """
    Provides credentials as loaded and parsed from
    provided token

    Parameters
    ----------
    token_path : str
        posix file path to token

    scopes : list[str]
        list of calendar scopes for which the
        pointed to token is valid

    Return
    ------
    Credentials
        the constructed credentials
    """

    return Credentials.from_authorized_user_file(
        filename=token_path,
        scopes=scopes,
    )


def is_creds_file(credentials_path):
    """
    Determine if provided posix file path
    to credentials file is valid

    Parameters
    ----------
    credentials_path : str
        posix file path to credentials

    Return
    ------
    bool
        True if file exists else False
    """

    return os.path.exists(credentials_path)


def is_stale_creds(creds):
    """
    Determine if provided credentials need
    be refreshed

    Parameters
    ----------
    credentials_path : str
        posix file path to credentials

    Return
    ------
    bool
        True if file exists else False
    """

    return creds and creds.expired and creds.refresh_token


def is_creds_valid(creds):
    """
    Validate provided credentials

    Parameters
    ----------
    creds : Credentials
        credentials to google api

    Return
    ------
    bool
        True if credentials valid else
        False
    """

    return creds and creds.valid


def is_token_file(token_path):
    """
    Determine if provided posix file path
    to token file is valid

    Parameters
    ----------
    token_path : str
        posix file path to token

    Return
    ------
    bool
        True if file exists else False
    """

    return os.path.exists(token_path)


def re_authenticate(creds, token_path, credentials_path, scopes):
    """
    Re-Authenticate provided credentials

    Parameters
    ----------
    creds : Credentials
        credentials to google api

    token_path : str
        posix file path to token

    credentials_path : str
        posix file path to credentials

    scopes : list[str]
        list of calendar scopes for which
        the pointed to token is valid

    Return
    ------
    Credentials
        the constructed credentials
    """

    if is_stale_creds(creds):
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            client_secrets_file=credentials_path,
            scopes=scopes,
        )
        creds = flow.run_local_server(port=0)
    return creds


def save_re_authecation(creds, token_path):
    """
    Save re-athenticated credentials for file

    Parameters
    ----------
    creds : Credentials
        credentials to google api

    token_path : str
        posix file path to token

    Return
    ------
    Credentials
        the constructed credentials
    """

    with open(token_path, "w") as token:
        token.write(creds.to_json())


def authenticate():
    """
    Athenticate user credentials assuming credentials file
    provided. For details please refer to README

    Parameters
    ----------
    creds : Credentials
        credentials to google api

    token_path : str
        posix file path to token

    Return
    ------
    Credentials
        the constructed credentials
    """

    config.create_working_directories()

    credentials_path = config.FILENAMES["credentials"]
    token_path = config.FILENAMES["token"]

    if not is_creds_file(credentials_path):
        raise FileNotFoundError("Credentials not found. Please see `README.md`")

    creds = (
        load_creds_from_file(token_path, config.SCOPES)
        if is_token_file(token_path)
        else None
    )

    if not is_creds_valid(creds):
        creds = re_authenticate(creds, token_path, credentials_path, config.SCOPES)
        save_re_authecation(creds, token_path)

    return creds


if __name__ == "__main__":
    creds = authenticate()
    print(creds)
