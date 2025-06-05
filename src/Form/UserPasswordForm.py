from typing import TypeVar

from Enum.Color import Color
from Form.BaseClasses.Form import Form
from Models.User import User
from View.UserInterfaceAlert import UserInterfaceAlert
from View.UserInterfaceFlow import UserInterfaceFlow
from View.UserInterfacePrompt import UserInterfacePrompt
from View.Validations.NotBlankValidation import NotBlankValidation
from View.Validations.OnlyLetterValidation import OnlyLetterValidation
from View.Validations.PasswordValidation import PasswordValidation
from View.Validations.UsernameValidation import UsernameValidation


class UserPasswordForm(Form):

    @staticmethod
    def get_form(ui: UserInterfaceFlow, existing: User = None) -> UserInterfaceFlow:
        ui.add(UserInterfacePrompt(
            prompt_text="Nieuw wachtwoord",
            memory_key="password",
            value=None,
            validations=[NotBlankValidation(), PasswordValidation()])
        )

        return ui
