from typing import TypeVar

from Enum.Color import Color
from Form.BaseClasses.Form import Form
from View.UserInterfaceAlert import UserInterfaceAlert
from View.UserInterfaceFlow import UserInterfaceFlow
from View.UserInterfacePrompt import UserInterfacePrompt
from View.Validations.EmailValdation import EmailValidation
from View.Validations.GenderValidation import GenderValidation
from View.Validations.LengthValdation import LengthValidation
from View.Validations.NotBlankValdation import NotBlankValidation
from View.Validations.NumberValdation import NumberValidation
from View.Validations.OnlyLetterValdation import OnlyLetterValidation
from View.Validations.OnlyNumberValdation import OnlyNumberValidation
from View.Validations.ZipcodeValdation import ZipcodeValidation


class MemberForm(Form):

    T = TypeVar("T")

    @staticmethod
    def get_form(ui: UserInterfaceFlow, existing: T = None) -> UserInterfaceFlow:
        ui.add(UserInterfaceAlert(text="Voer de gegevens in van de nieuwe member", color=Color.WHITE))
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
            prompt_text="Leeftijd",
            memory_key="age",
            value=existing.age if existing else None,
            validations=[NotBlankValidation(), NumberValidation()])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Gewicht in (kg)",
            memory_key="weight",
            value=existing.weight if existing else None,
            validations=[NotBlankValidation(), NumberValidation()])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Geslacht (m/v/x)",
            memory_key="gender",
            value=existing.gender if existing else None,
            validations=[NotBlankValidation(), GenderValidation()])
        )

        ui.add(UserInterfaceAlert(text="==============", color=Color.WHITE))

        ui.add(UserInterfaceAlert(text="Voer de contact gegevens in van de nieuwe member", color=Color.WHITE))

        # TODO: Check uniqueness
        ui.add(UserInterfacePrompt(
            prompt_text="E-mailadres",
            memory_key="emailAddress",
            value=existing.emailAddress if existing else None,
            validations=[NotBlankValidation(), EmailValidation()])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Telefoon nummer (+31-6-NNNNNNNN) +31-6-",
            memory_key="phoneNumber",
            value=existing.phoneNumber if existing else None,
            validations=[NotBlankValidation(), OnlyNumberValidation(), LengthValidation(8)])
        )

        ui.add(UserInterfaceAlert(text="==============", color=Color.WHITE))

        ui.add(UserInterfaceAlert(text="Voer de adres gegevens in van de nieuwe member", color=Color.WHITE))

        ui.add(UserInterfacePrompt(
            prompt_text="Straatnaam",
            memory_key="streetName",
            value=existing.streetName if existing else None,
            validations=[NotBlankValidation(), OnlyLetterValidation()])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Huisnummer",
            memory_key="houseNumber",
            value=existing.houseNumber if existing else None,
            validations=[NotBlankValidation(), NumberValidation()])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Postcode (XXXXAB)",
            memory_key="zipCode",
            value=existing.zipCode if existing else None,
            validations=[NotBlankValidation(), ZipcodeValidation()])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Stad",
            memory_key="city",
            value=existing.city if existing else None,
            validations=[NotBlankValidation(), OnlyLetterValidation()])
        )

        return ui