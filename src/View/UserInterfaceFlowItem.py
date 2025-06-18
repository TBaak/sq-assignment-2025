from abc import abstractmethod, ABC

from Enum.Color import Color


class UserInterfaceFlowItem(ABC):

    consoleTitle: str = "Urban Mobility Management Systeem"
    consoleColor: Color = Color.WHITE
    memoryKey: str = None

    @abstractmethod
    def render(self, is_retrying: bool = False):
        pass
