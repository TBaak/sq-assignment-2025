from typing import TypeVar

from Enum.Color import Color
from Form.BaseClasses.Form import Form
from Models.User import User
from View.UserInterfaceAlert import UserInterfaceAlert
from View.UserInterfaceFlow import UserInterfaceFlow
from View.UserInterfacePrompt import UserInterfacePrompt
from View.Validations.MaxLengthValidation import MaxLengthValidation
from View.Validations.NotBlankValidation import NotBlankValidation
from View.Validations.OnlyLetterValidation import OnlyLetterValidation
from View.Validations.UsernameValidation import UsernameValidation


class UserForm(Form):

    @staticmethod
    def get_form(ui: UserInterfaceFlow, existing: User = None) -> UserInterfaceFlow:
        ui.add(UserInterfaceAlert(text="Voer de gegevens in van de user", color=Color.WHITE))
        ui.add(UserInterfacePrompt(
            prompt_text="Voornaam",
            memory_key="first_name",
            value=existing.first_name if existing else None,
            validations=[NotBlankValidation(), OnlyLetterValidation(), MaxLengthValidation(50)])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Achternaam",
            memory_key="last_name",
            value=existing.last_name if existing else None,
            validations=[NotBlankValidation(), OnlyLetterValidation(), MaxLengthValidation(50)])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Username "
                        "(moet tussen 8 en 10 karakters lang zijn, beginnen met een letter of "
                        "underscore (_), en alleen letters, cijfers, underscores (_), apostrofes ('), "
                        "en punten (.) bevatten.)",
            memory_key="username",
            value=existing.username if existing else None,
            validations=[NotBlankValidation(), UsernameValidation()])
        )


        return ui
