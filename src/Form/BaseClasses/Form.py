from typing import TypeVar

from View.UserInterfaceFlow import UserInterfaceFlow


class Form:

    T = TypeVar("T")

    @staticmethod
    def get_form(ui: UserInterfaceFlow, existing: T = None):
        raise NotImplementedError("Subclasses must implement abstract method")