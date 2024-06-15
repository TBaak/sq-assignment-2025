from typing import TypeVar

from Enum.Color import Color
from Form.BaseClasses.Form import Form
from View.UserInterfaceAlert import UserInterfaceAlert
from View.UserInterfaceFlow import UserInterfaceFlow
from View.UserInterfacePrompt import UserInterfacePrompt
from View.Validations.NotBlankValdation import NotBlankValidation
from View.Validations.OnlyLetterValdation import OnlyLetterValidation
from View.Validations.UsernameValdation import UsernameValidation


class UserForm(Form):
    T = TypeVar("T")

    @staticmethod
    def get_form(ui: UserInterfaceFlow, existing: T = None) -> UserInterfaceFlow:
        ui.add(UserInterfaceAlert(text="Voer de gegevens in van de nieuwe user", color=Color.WHITE))
        ui.add(UserInterfacePrompt(
            prompt_text="Voornaam",
            memory_key="firstName",
            value=existing.firstName if existing else None,
            validations=[NotBlankValidation(), OnlyLetterValidation()])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Achternaam",
            memory_key="lastName",
            value=existing.lastName if existing else None,
            validations=[NotBlankValidation(), OnlyLetterValidation()])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Username"
                        "(Username moet tussen 8 en 10 karakters lang zijn, beginnen met een letter of "
                        "underscore (_), en alleen letters, cijfers, underscores (_), apostrofes ('), "
                        "en punten (.) bevatten.)",
            memory_key="username",
            value=existing.username if existing else None,
            validations=[NotBlankValidation(), UsernameValidation()])
        )


        return ui
