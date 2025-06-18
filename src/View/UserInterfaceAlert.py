from os import system

from Enum.Color import Color
from View.UserInterfaceFlowItem import UserInterfaceFlowItem


class UserInterfaceAlert(UserInterfaceFlowItem):

    def __init__(self, text: str, color: Color = None):
        self.text = text
        if color is not None:
            self.consoleColor = color

    def render(self, is_retrying: bool = False):
        system("title " + self.consoleTitle)
        print(self.consoleColor.value + self.text + Color.ENDC.value)
        return True, None
