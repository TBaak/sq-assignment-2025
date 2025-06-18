import getpass
import sys
from os import system
from time import sleep

from Enum.LogType import LogType
from Repository.LogRepository import LogRepository
from Security.SecurityHelper import SecurityHelper
from View.UserInterfaceAlert import UserInterfaceAlert
from Enum.Color import Color
from View.UserInterfaceFlow import UserInterfaceFlow
from View.UserInterfaceFlowItem import UserInterfaceFlowItem


class UserInterfacePrompt(UserInterfaceFlowItem):

    def __init__(self, prompt_text: str, memory_key: str = "default", validations=None, is_password: bool = False,
                 value: str = None):
        if validations is None:
            validations = []
        self.promptText = prompt_text + (f" [{value}]" if (value is not None) else "") + ": "
        self.isPassword = is_password
        self.memoryKey = memory_key
        self.validations = validations
        self.value = value

    def render(self, is_retrying: bool = False):

        if self.isPassword:
            inp = getpass.getpass(self.promptText)
        else:
            inp = input(self.promptText)

        if '\x00' in inp:
            logged_in_user = SecurityHelper.get_logged_in_user()

            LogRepository.log(LogType.NullByteInput, f"User: {logged_in_user.id}" if logged_in_user else "")

            UserInterfaceFlow.quick_run(
                UserInterfaceAlert("Verdachte invoer, u wordt nu uitgelogd", Color.FAIL),
                1
            )
            exit(1)

        if inp == "" and self.value is not None:
            return True, self.value

        valid = self.validate(inp)
        return valid, inp

    def validate(self, inp: str):
        for validation in self.validations:
            is_valid, message = validation.validate(inp)
            if not is_valid:
                UserInterfacePrompt.render_validation_error(message)
                return False
        return True

    @staticmethod
    def render_validation_error(message: str):
        UserInterfaceFlow.clear_line()
        UserInterfaceAlert(text=message, color=Color.FAIL).render()
        sleep(2)
        UserInterfaceFlow.clear_line()
