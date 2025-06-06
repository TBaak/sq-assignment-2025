from typing import TypeVar

from Enum.Color import Color
from Form.BaseClasses.Form import Form
from Models.Scooter import Scooter
from Models.Traveller import Traveller
from View.UserInterfaceAlert import UserInterfaceAlert
from View.UserInterfaceFlow import UserInterfaceFlow
from View.UserInterfacePrompt import UserInterfacePrompt
from View.Validations.AlphaNumericValidation import AlphaNumericValidation
from View.Validations.CityValidation import CityValidation
from View.Validations.CoordinateValidation import CoordinateValidation
from View.Validations.DateValidation import DateValidation
from View.Validations.EmailValidation import EmailValidation
from View.Validations.GenderValidation import GenderValidation
from View.Validations.LengthValidation import LengthValidation
from View.Validations.MaxLengthValidation import MaxLengthValidation
from View.Validations.MinLengthValidation import MinLengthValidation
from View.Validations.NotBlankValidation import NotBlankValidation
from View.Validations.NumberMaxValidation import NumberMaxValidation
from View.Validations.NumberMinValidation import NumberMinValidation
from View.Validations.NumberValidation import NumberValidation
from View.Validations.OnlyLetterValidation import OnlyLetterValidation
from View.Validations.OnlyNumberValidation import OnlyNumberValidation
from View.Validations.YesNoValidation import YesNoValidation
from View.Validations.ZipcodeValidation import ZipcodeValidation


class ScooterFormFull(Form):

    @staticmethod
    def get_form(ui: UserInterfaceFlow, existing: Scooter = None) -> UserInterfaceFlow:
        ui.add(UserInterfaceAlert(text="Voer de gegevens in van de scooter", color=Color.WHITE))
        ui.add(UserInterfacePrompt(
            prompt_text="Merk",
            memory_key="brand",
            value=existing.brand if existing else None,
            # TODO Allow names like Björk
            validations=[NotBlankValidation(), OnlyLetterValidation(), MaxLengthValidation(50)])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Model",
            memory_key="model",
            value=existing.model if existing else None,
            # TODO Allow names like Björk
            validations=[NotBlankValidation(), OnlyLetterValidation(), MaxLengthValidation(50)])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Serienummer (10-17 karakters)",
            memory_key="serial_number",
            value=existing.serial_number if existing else None,
            validations=[AlphaNumericValidation(), MinLengthValidation(10), MaxLengthValidation(17)])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Maximale snelheid (km/h)",
            memory_key="top_speed",
            value=existing.top_speed if existing else None,
            validations=[NumberValidation(), MinLengthValidation(1), MaxLengthValidation(3)])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Batterij capaciteit (Wh)",
            memory_key="battery_capacity",
            value=existing.battery_capacity if existing else None,
            validations=[NumberValidation(), MinLengthValidation(1), MaxLengthValidation(5)])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Huidige batterij percentage (0-100)",
            memory_key="state_of_charge",
            value=existing.state_of_charge if existing else None,
            validations=[NumberValidation(), MinLengthValidation(1), MaxLengthValidation(3), NumberMaxValidation(100), NumberMinValidation(0)])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Doel batterij percentage minimaal (0-100)",
            memory_key="target_range_soc_min",
            value=existing.target_range_soc_min if existing else None,
            validations=[NumberValidation(), MinLengthValidation(1), MaxLengthValidation(3), NumberMaxValidation(100), NumberMinValidation(0)])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Doel batterij percentage maximaal (0-100)",
            memory_key="target_range_soc_max",
            value=existing.target_range_soc_max if existing else None,
            validations=[NumberValidation(), MinLengthValidation(1), MaxLengthValidation(3), NumberMaxValidation(100), NumberMinValidation(0)])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Locatie (latitude longitude bijv. \"51.92250 4.47917\", 5 decimalen)",
            memory_key="location",
            value=existing.location_lat + ' ' + existing.location_lng if existing else None,
            validations=[NotBlankValidation(), CoordinateValidation()])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="In dienst (y/n)",
            memory_key="out_of_service_status",
            value=existing.out_of_service_status if existing else None,
            validations=[NotBlankValidation(), YesNoValidation()])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Kilometerstand",
            memory_key="mileage",
            value=existing.mileage if existing else None,
            validations=[NumberValidation(), MinLengthValidation(1), MaxLengthValidation(5), NumberMaxValidation(500_000),
                         NumberMinValidation(0)])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Datum laatste onderhoud (YYYY-MM-DD)",
            memory_key="last_maintenance",
            value=existing.last_maintenance if existing else None,
            validations=[NotBlankValidation(), DateValidation()])
        )

        return ui