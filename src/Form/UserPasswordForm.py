from typing import TypeVar

from Enum.Color import Color
from Form.BaseClasses.Form import Form
from View.UserInterfaceAlert import UserInterfaceAlert
from View.UserInterfaceFlow import UserInterfaceFlow
from View.UserInterfacePrompt import UserInterfacePrompt
from View.Validations.NotBlankValdation import NotBlankValidation
from View.Validations.OnlyLetterValdation import OnlyLetterValidation
from View.Validations.PasswordValdation import PasswordValidation
from View.Validations.UsernameValdation import UsernameValidation


class UserPasswordForm(Form):
    T = TypeVar("T")

    @staticmethod
    def get_form(ui: UserInterfaceFlow, existing: T = None) -> UserInterfaceFlow:
        ui.add(UserInterfaceAlert(text="Voer de gegevens in van de nieuwe user", color=Color.WHITE))
        ui.add(UserInterfacePrompt(
            prompt_text="Nieuw wachtwoord",
            memory_key="password",
            value=None,
            validations=[NotBlankValidation(), PasswordValidation()])
        )

        return ui
