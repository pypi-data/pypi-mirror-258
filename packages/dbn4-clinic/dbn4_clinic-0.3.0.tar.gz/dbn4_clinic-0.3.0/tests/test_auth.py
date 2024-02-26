from unittest.mock import MagicMock
from unittest.mock import patch
from unittest import TestCase
from unittest import main
from unittest import skip
from pathlib import Path
import pathlib
import sys
import os


from google.auth.exceptions import RefreshError
from googleapiclient.discovery import Resource


sys.path.append(pathlib.Path.cwd().as_posix())


from utils import auth


class TestAuth(TestCase):

    @patch("utils.auth.is_creds_file", return_value=False)
    def test_no_creds_exists(self, mock_credentials):
        """Assert user is informed if no credentials found"""

        with self.assertRaises(FileNotFoundError) as error:
            auth.authenticate()

        exception = str(error.exception).lower()
        self.assertTrue("credentials not found" in exception)
        self.assertTrue("readme.md" in exception)

    @patch("builtins.open")
    @patch("utils.auth.InstalledAppFlow.from_client_secrets_file")
    @patch("utils.auth.is_token_file", return_value=False)
    @patch("utils.auth.is_creds_file", return_value=True)
    def test_no_token_exists(self, mock_credentials, mock_token, mock_flow, mock_open):
        """Assert token is created if no token found"""

        auth.authenticate()

        expected_path = Path.home().joinpath(".code_clinic/credentials/token.json")
        mock_open.assert_called_once_with(expected_path.as_posix(), "w")

    @patch("utils.auth.is_creds_valid", return_value=True)
    @patch("utils.auth.load_creds_from_file", return_value="mocked creds")
    @patch("utils.auth.is_token_file", return_value=True)
    @patch("utils.auth.is_creds_file", return_value=True)
    def test_has_token(self, mock_credentials, mock_token, mock_load, mock_valid):
        """Assert token is returned if token found"""

        self.assertEqual(auth.authenticate(), "mocked creds")

    @patch("google.oauth2.credentials.Credentials")
    def test_is_connected_when_connected(self, mock_creds):
        connected = auth.is_connected(mock_creds)

        mock_creds.refresh.assert_called_once()
        self.assertTrue(connected)

    @patch("google.oauth2.credentials.Credentials")
    def test_is_connected_when_not_connected(self, mock_creds):
        mock_creds.refresh.side_effect = RefreshError
        connected = auth.is_connected(mock_creds)

        mock_creds.refresh.assert_called_once()
        self.assertFalse(connected)

    @skip
    @patch("googleapiclient.discovery.build")
    @patch("google.oauth2.credentials.Credentials")
    def test_build_service(self, mock_creds, mock_build):
        auth.build_service(mock_creds)
        mock_build.assert_called_once()


if __name__ == "__main__":
    main()
