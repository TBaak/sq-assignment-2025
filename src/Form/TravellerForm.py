from typing import TypeVar

from Enum.Color import Color
from Form.BaseClasses.Form import Form
from Models.Traveller import Traveller
from View.UserInterfaceAlert import UserInterfaceAlert
from View.UserInterfaceFlow import UserInterfaceFlow
from View.UserInterfacePrompt import UserInterfacePrompt
from View.Validations.CityValidation import CityValidation
from View.Validations.DateValidation import DateValidation
from View.Validations.EmailValidation import EmailValidation
from View.Validations.GenderValidation import GenderValidation
from View.Validations.LengthValidation import LengthValidation
from View.Validations.MaxLengthValidation import MaxLengthValidation
from View.Validations.NoSpecialCharsValidation import NoSpecialCharsValidation
from View.Validations.NotBlankValidation import NotBlankValidation
from View.Validations.NumberValidation import NumberValidation
from View.Validations.OnlyLetterValidation import OnlyLetterValidation
from View.Validations.OnlyNumberValidation import OnlyNumberValidation
from View.Validations.ZipcodeValidation import ZipcodeValidation


class TravellerForm(Form):

    @staticmethod
    def get_form(ui: UserInterfaceFlow, existing: Traveller = None) -> UserInterfaceFlow:
        ui.add(UserInterfaceAlert(text="Voer de gegevens in van de traveller", color=Color.WHITE))
        ui.add(UserInterfacePrompt(
            prompt_text="Voornaam",
            memory_key="first_name",
            value=existing.first_name if existing else None,
            # TODO Allow names like Björk
            validations=[NotBlankValidation(), OnlyLetterValidation(), MaxLengthValidation(50)])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Achternaam",
            memory_key="last_name",
            value=existing.last_name if existing else None,
            # TODO Allow names like Björk
            validations=[NotBlankValidation(), OnlyLetterValidation(), MaxLengthValidation(50)])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Geboorte datum (YYYY-MM-DD)",
            memory_key="dob",
            value=existing.dob if existing else None,
            validations=[NotBlankValidation(), DateValidation()])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Geslacht (m/v/x)",
            memory_key="gender",
            value=existing.gender if existing else None,
            validations=[NotBlankValidation(), GenderValidation()])
        )

        ui.add(UserInterfaceAlert(text="==============", color=Color.WHITE))

        ui.add(UserInterfaceAlert(text="Voer de contact gegevens in van de nieuwe traveller", color=Color.WHITE))

        ui.add(UserInterfacePrompt(
            prompt_text="E-mailadres",
            memory_key="email_address",
            value=existing.email_address if existing else None,
            validations=[NotBlankValidation(), EmailValidation(), MaxLengthValidation(254)])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Telefoon nummer (+31-6-NNNNNNNN) +31-6-",
            memory_key="phone_number",
            value=existing.phone_number if existing else None,
            validations=[NotBlankValidation(), OnlyNumberValidation(), LengthValidation(8)])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Rijbewijs nummer", # Format
            memory_key="driving_license_number",
            value=existing.driving_license_number if existing else None,
            validations=[NotBlankValidation(), OnlyNumberValidation(), LengthValidation(8)]) # TODO Check requirements for driving license number
        )

        ui.add(UserInterfaceAlert(text="==============", color=Color.WHITE))

        ui.add(UserInterfaceAlert(text="Voer de adres gegevens in van de nieuwe traveller", color=Color.WHITE))

        ui.add(UserInterfacePrompt(
            prompt_text="Straatnaam",
            memory_key="street_name",
            value=existing.street_name if existing else None,
            validations=[NotBlankValidation(), OnlyLetterValidation(), MaxLengthValidation(100)])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Huisnummer",
            memory_key="house_number",
            value=existing.house_number if existing else None,
            validations=[NotBlankValidation(), NoSpecialCharsValidation(), MaxLengthValidation(5)])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Postcode (XXXXAB)",
            memory_key="zip_code",
            value=existing.zip_code if existing else None,
            validations=[NotBlankValidation(), ZipcodeValidation()])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Stad "
                        "(Den Haag, Rotterdam, Amsterdam, Utrecht, Eindhoven, Tilburg, Groningen, Almere, Breda, Nijmegen)",
            memory_key="city",
            value=existing.city if existing else None,
            validations=[NotBlankValidation(), CityValidation()])
        )

        return ui