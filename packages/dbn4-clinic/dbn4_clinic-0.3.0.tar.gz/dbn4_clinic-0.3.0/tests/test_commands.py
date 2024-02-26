from unittest.mock import patch
from unittest.mock import Mock
from unittest import TestCase
from unittest import main
from unittest import skip


from commands.commands import cmd_exit
from commands.commands import cmd_invalid


class TestCommands(TestCase):

    def setUp(self):
        self.commands = [
            "cmd_view_clinic_calendar",
            "cmd_view_personal_calendar",
            "cmd_book_assistance",
            "cmd_volunteer_assistance",
            "cmd_cancel_assistance_session",
            "cmd_cancel_volunteer_session",
            "cmd_configure",
            "cmd_validate_connection",
            "cmd_invalid",
        ]

    @staticmethod
    def get_output(mock_print):
        calls = mock_print.call_args_list
        return " ".join(str(call_.args) for call_ in calls).lower()

    @patch("builtins.print")
    def test_cmd_exit(self, mock_print):
        with self.assertRaises(SystemExit):
            cmd_exit()

        output = self.get_output(mock_print)

        self.assertTrue("goodbye" in output)

    @patch("builtins.print")
    def test_cmd_invalid(self, mock_print):
        invalid_options = ["", "invalid", "x29", "-1", 0]

        for option in invalid_options:
            cmd_invalid(option)

        output = self.get_output(mock_print)

        for option in invalid_options:
            self.assertTrue(f"no such option: '{option}'" in output)
            self.assertTrue("please select again" in output)

    @skip
    def test_view_clinic_calendar(self):
        for command in self.commands:
            with patch(f"commands.commands.{command}") as cmd:
                cmd()


if __name__ == "__main__":
    main()
