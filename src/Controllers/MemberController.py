from Enum.Color import Color
from Helpers.UserHelper import UserHelper
from Models.Member import Member
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


class MemberController:

    def add_member(self):
        UserHelper.has_permission(None)  # TODO: Implement this

        ui = UserInterfaceFlow()
        ui.add(UserInterfaceAlert(text="Member toevoegen", color=Color.OKBLUE))
        ui.add(UserInterfaceAlert(text="Voer de gegevens in van de nieuwe member", color=Color.WHITE))

        ui.add(UserInterfacePrompt(
            prompt_text="Voornaam: ",
            memory_key="firstName",
            validations=[NotBlankValidation(), OnlyLetterValidation()])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Achternaam: ",
            memory_key="lastName",
            validations=[NotBlankValidation(), OnlyLetterValidation()])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Leeftijd: ",
            memory_key="age",
            validations=[NotBlankValidation(), NumberValidation()])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Gewicht in (kg): ",
            memory_key="weight",
            validations=[NotBlankValidation(), NumberValidation()])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Geslacht (m/v/x): ",
            memory_key="gender",
            validations=[NotBlankValidation(), GenderValidation()])
        )

        ui.add(UserInterfaceAlert(text="==============", color=Color.WHITE))

        ui.add(UserInterfaceAlert(text="Voer de contact gegevens in van de nieuwe member", color=Color.WHITE))

        # TODO: Check uniqueness
        ui.add(UserInterfacePrompt(
            prompt_text="E-mailadres: ",
            memory_key="emailAddress",
            validations=[NotBlankValidation(), EmailValidation()])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Telefoon nummer (+31-6-NNNNNNNN): +31-6-",
            memory_key="phoneNumber",
            validations=[NotBlankValidation(), OnlyNumberValidation(), LengthValidation(8)])
        )

        ui.add(UserInterfaceAlert(text="==============", color=Color.WHITE))

        ui.add(UserInterfaceAlert(text="Voer de adres gegevens in van de nieuwe member", color=Color.WHITE))

        ui.add(UserInterfacePrompt(
            prompt_text="Straatnaam: ",
            memory_key="streetName",
            validations=[NotBlankValidation(), OnlyLetterValidation()])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Huisnummer: ",
            memory_key="houseNumber",
            validations=[NotBlankValidation(), NumberValidation()])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Postcode (XXXXAB): ",
            memory_key="zipCode",
            validations=[NotBlankValidation(), ZipcodeValidation()])
        )

        ui.add(UserInterfacePrompt(
            prompt_text="Stad: ",
            memory_key="city",
            validations=[NotBlankValidation(), OnlyLetterValidation()])
        )

        fields = ui.run()

        member = Member()
        member.populate(list(fields.values()), list(fields.keys()))

        print(fields)
        print("TODO: Add member to database")

        pass
