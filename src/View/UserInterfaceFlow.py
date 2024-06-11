import sys
from os import name, system
from time import sleep

from View.UserInterfaceFlowItem import UserInterfaceFlowItem


class UserInterfaceFlow:

    def __init__(self):
        self.screens = []
        self.ranScreens = []
        self.currentScreen = 0
        self.memory = {}

    def add(self, flow_item: UserInterfaceFlowItem):
        self.screens.append(flow_item)
        return self

    def run(self):
        self.memory = {}
        self.currentScreen = 0
        self.ranScreens = [False] * len(self.screens)

        self.clear()

        # Fetch the first item in screen as long if it is not empty
        while True:

            if self.currentScreen == len(self.screens):
                break

            current = self.screens[self.currentScreen]

            has_ran = self.ranScreens[self.currentScreen]

            if not has_ran:
                self.ranScreens[self.currentScreen] = True

            is_valid, value = current.render(has_ran)
            if is_valid:
                if current.memoryKey:
                    self.memory[current.memoryKey] = value
                self.currentScreen += 1

        return self.memory

    @staticmethod
    def quick_run(screen: UserInterfaceFlowItem, sleep_time: int = 3):
        UserInterfaceFlow.clear()
        screen.render()
        if sleep_time:
            sleep(sleep_time)

    @staticmethod
    def clear():
        # for windows
        if name == 'nt':
            _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')

    @staticmethod
    def clear_line(lines_up: int = 1):
        CURSOR_UP_ONE = '\x1b[1A'
        ERASE_LINE = '\x1b[2K'
        CURSOR_DOWN_ONE = '\x1b[1B'

        # Move the cursor up and clear each line
        for _ in range(lines_up):
            sys.stdout.write(CURSOR_UP_ONE)

        sys.stdout.write(ERASE_LINE)

        # Move the cursor back to the original position
        if lines_up > 1:
            for _ in range(lines_up):
                sys.stdout.write(CURSOR_DOWN_ONE)
