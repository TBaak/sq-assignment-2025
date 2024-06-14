from Controllers.MenuController import MenuController
from DTO.LoginError import LoginError
from Enum.Color import Color
from Enum.LogType import LogType
from Repository.LogRepository import LogRepository
from Security.SecurityHelper import SecurityHelper
from Models.User import User
from Repository.UserRepository import UserRepository
from Security.Enum.Role import Role
from Service.HashService import HashService
from View.UserInterfaceAlert import UserInterfaceAlert
from View.UserInterfaceFlow import UserInterfaceFlow
from View.UserInterfacePrompt import UserInterfacePrompt
from View.Validations.NotBlankValdation import NotBlankValidation


class LoginController:
    __login_tries = 0

    def __init__(self):
        self.__login_tries = 0

    def login(self):
        # 'super_admin' & 'Admin_123?'

        self.__login_tries += 1

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

        # HARDCODED SUPER ADMIN
        if result["username"] == "super_admin" and result["password"] == "Admin_123?":
            self.__login_superadmin()

            LogRepository.log(LogType.SuccessfulLogin)

            mc = MenuController()
            mc.menu()
            return

        username = result["username"]
        password = result["password"]

        loginResult = UserRepository.find_by_credentials(username, password)

        user = loginResult[0]
        error_reason = loginResult[1]

        if user is None:

            if self.__login_tries >= 3:
                LogRepository.log(LogType.UnsuccessfulLoginSuspicious,
                                  "Multiple usernames and passwords are tried in a row")

                UserInterfaceFlow.quick_run(
                    UserInterfaceAlert("Te vaak fout ingelogd, afsluiten", Color.FAIL),
                    2
                )
                return

            UserInterfaceFlow.quick_run(
                UserInterfaceAlert("Incorrecte inloggegevens", Color.FAIL),
                2
            )

            if error_reason == LoginError.NotFound:
                LogRepository.log(LogType.UnsuccessfulLogin,
                                  f"username: “{username}” is used for a login attempt with a wrong password")

            if error_reason == LoginError.BadCredentials:
                LogRepository.log(LogType.UnsuccessfulLogin,
                                  f"username: “{username}” not in the database")

            self.login()
            return

        if not SecurityHelper.set_logged_in_user(user):

            LogRepository.log(LogType.UnsuccessfulLogin,
                              f"username: “{username}” user is not correct in database")

            UserInterfaceFlow.quick_run(
                UserInterfaceAlert("Er ging iets mis, probeer het nog eens", Color.FAIL),
                2
            )
            self.login()
            return

        LogRepository.log(LogType.SuccessfulLogin)

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
        superAdmin.role = Role["SUPER_ADMIN"].name

        SecurityHelper.set_logged_in_user(superAdmin)

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert(f"Ingelogd als super admin", Color.OKGREEN)
        )
