"""Test project entry point"""

from unittest.mock import MagicMock
from unittest.mock import patch
from unittest import TestCase
from unittest import main
from unittest import skip
import pathlib
import sys


sys.path.append(pathlib.Path.cwd().as_posix())


from main import main


class TestMain(TestCase):

    def setUp(self):
        self.mock_creds = MagicMock()
        self.mock_service = MagicMock()

    @staticmethod
    def get_output(mock_print):
        """Provide mocked print out as a lowercased string"""

        calls = mock_print.call_args_list
        return " ".join(str(call_.args) for call_ in calls).lower()

    @skip
    @patch("builtins.print")
    @patch("builtins.input", side_effects=["invalid inputs", "9"])
    def test_execute_false_command(self, mock_input, mock_print):
        """Assert user informed of invalid selction"""

        with self.assertRaises(SystemExit):
            main(self.mock_creds, self.mock_service)

        output = self.get_output(mock_print)

        self.assertTrue("no such command: 'invalid'" in output)
        self.assertTrue("please select again" in output)
        self.assertTrue("exiting" in output)

    @patch("builtins.print")
    @patch("builtins.input", return_value="9")
    def test_execute_exit(self, mock_input, mock_print):
        """Assert exit kills the program"""

        with self.assertRaises(SystemExit):
            main(self.mock_creds, self.mock_service)

        output = TestMain.get_output(mock_print)

        self.assertTrue("goodbye" in output)


if __name__ == "__main__":
    main()
