from Enum.Color import Color
from Helpers.UserHelper import UserHelper
from Repository.UserRepository import UserRepository
from View.UserInterfaceAlert import UserInterfaceAlert
from View.UserInterfaceFlow import UserInterfaceFlow
from View.UserInterfacePrompt import UserInterfacePrompt
from View.Validations.NotBlankValdation import NotBlankValidation


class LoginController:

    def login(self):
        # 'super_admin' & 'Admin_123?'

        ui = UserInterfaceFlow()

        ui.add(
            UserInterfaceAlert(
                text="Inloggen",
                color=Color.OKBLUE
            )
        )
        ui.add(
            UserInterfacePrompt(
                prompt_text="Gebruikersnaam: ",
                memory_key="username",
                validations=[NotBlankValidation()]
            )
        )
        ui.add(
            UserInterfacePrompt(
                prompt_text="Wachtwoord (invoer verborgen): ",
                memory_key="password",
                is_password=True,
                validations=[NotBlankValidation()]
            )
        )

        result = ui.run()

        user = UserRepository.find_by_credentials(result["username"], result["password"])

        self.login()
