from Controllers.MenuController import MenuController
from Enum.Color import Color
from Helpers.UserHelper import UserHelper
from Models.User import User
from Repository.UserRepository import UserRepository
from Service.HashService import HashService
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
                prompt_text="Gebruikersnaam",
                memory_key="username",
                validations=[NotBlankValidation()]
            )
        )
        ui.add(
            UserInterfacePrompt(
                prompt_text="Wachtwoord (invoer verborgen)",
                memory_key="password",
                is_password=True,
                validations=[NotBlankValidation()]
            )
        )

        result = ui.run()

        # HARDCODES SUPER ADMIN
        if result["username"] == "super_admin" and result["password"] == "Admin_123?":
            self.__login_superadmin()

            mc = MenuController()
            mc.menu()
            return

        user = UserRepository.find_by_credentials(result["username"], result["password"])

        if user is None:
            UserInterfaceFlow.quick_run(
                UserInterfaceAlert("Incorrecte inloggegevens", Color.FAIL),
                2
            )
            self.login()
            return

        UserHelper.set_logged_in_user(user)

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert(f"Welkom {user.username}", Color.OKGREEN)
        )

        mc = MenuController()
        mc.menu()

    def __login_superadmin(self):
        superAdmin = User()

        superAdmin.id = 0
        superAdmin.username = "super_admin"
        superAdmin.password = HashService.hash("Admin_123?")
        superAdmin.role = "super_admin"

        UserHelper.set_logged_in_user(superAdmin)

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert(f"Ingelogd als super admin", Color.OKGREEN)
        )

