from time import sleep

from View.UserInterfaceFlowItem import UserInterfaceFlowItem


class UserInterfaceSleep(UserInterfaceFlowItem):

    def __init__(self, sleep_time: int):
        self.sleepTime = sleep_time

    def render(self, is_retrying: bool = False):
        sleep(self.sleepTime)
        return True, None
