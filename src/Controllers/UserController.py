from datetime import datetime

from Enum.Color import Color
from Enum.LogType import LogType
from Enum.UserType import UserType
from Form.UserForm import UserForm
from Form.UserPasswordForm import UserPasswordForm
from Models.User import User
from Repository.LogRepository import LogRepository
from Repository.UserRepository import UserRepository
from Security.AuthorizationDecorator import Auth
from Security.Enum.Permission import Permission
from Security.Enum.Role import Role
from Security.SecurityHelper import SecurityHelper
from Service.HashService import HashService
from Service.IndexService import IndexService
from View.UserInterfaceAlert import UserInterfaceAlert
from View.UserInterfaceFlow import UserInterfaceFlow
from View.UserInterfacePrompt import UserInterfacePrompt
from View.UserInterfaceTable import UserInterfaceTable
from View.UserInterfaceTableRow import UserInterfaceTableRow
from View.Validations.NoSpecialCharsValidation import NoSpecialCharsValidation
from View.Validations.OnlyLetterValdation import OnlyLetterValidation


class UserController:

    @Auth.permission_required(Permission.UserServiceEngineerRead)
    def list_service_engineer_users(self, users: list[User] = None):

        UserInterfaceFlow.quick_run_till_next(
            UserInterfaceAlert("Service Engineer overzicht aan het laden...", Color.HEADER)
        )

        LogRepository.log(LogType.UserServiceEngineersRead)

        self.__show_users(Role.SERVICE_ENGINEER, users)

    @Auth.permission_required(Permission.UserSystemAdminRead)
    def list_system_admin_users(self, users: list[User] = None):

        UserInterfaceFlow.quick_run_till_next(
            UserInterfaceAlert("Systeem beheerder overzicht aan het laden...", Color.HEADER)
        )

        LogRepository.log(LogType.UserSystemAdminsRead)

        self.__show_users(Role.SYSTEM_ADMIN, users)

    def __show_users(self, role: Role, users: list[User] = None):

        header_type = "Service Engineer" if role.SERVICE_ENGINEER else "Systeem beheerder"
        header = f"{header_type} overzicht" if users is None else "Zoekresultaten"

        if users is None:
            users = UserRepository.find_all_by_role(role)

        rows = map(lambda u: [u.username, u.first_name, u.last_name, u.registration_date], users)
        rows = list(rows)

        for index, row in enumerate(rows):
            row.insert(0, index + 1)

        rows = list(map(lambda m_row: UserInterfaceTableRow(m_row), rows))

        rows.insert(0, UserInterfaceTableRow(
            ["#", "Username", "Voornaam", "Achternaam", "Registratie datum"]))

        ui = UserInterfaceFlow()
        ui.add(UserInterfaceAlert(header, Color.HEADER))
        ui.add(UserInterfaceTable(rows=rows, has_header=True))
        ui.add(UserInterfacePrompt(
            prompt_text="Geef het nummer om te bekijken of druk op Z om te zoeken of druk op ENTER om terug te gaan",
            memory_key="action"
        )
        )
        selection = ui.run()

        selected = selection["action"]

        if selected == "":
            return

        if selected.upper() == "Z":
            if role == Role.SERVICE_ENGINEER:
                return self.search_service_engineer_user()
            if role == Role.SYSTEM_ADMIN:
                return self.search_system_admin_user()

        user_index = int(selected) - 1

        try:
            selected_user = users[user_index]
        except IndexError:
            UserInterfaceFlow.quick_run(
                UserInterfaceAlert("Ongeldige keuze", Color.FAIL),
                1
            )
            return

        if role == Role.SYSTEM_ADMIN:
            self.show_system_admin_user(selected_user)

        if role == Role.SERVICE_ENGINEER:
            self.show_service_engineer_user(selected_user)

        return self.__show_users(role, users)

    @Auth.permission_required(Permission.UserServiceEngineerRead)
    def show_service_engineer_user(self, user: User):

        LogRepository.log(LogType.UserServiceEngineerRead)

        return self.__show_user(user)

    @Auth.permission_required(Permission.UserSystemAdminRead)
    def show_system_admin_user(self, user: User):

        LogRepository.log(LogType.UserSystemAdminRead)

        return self.__show_user(user)

    def __show_user(self, user: User):

        rows = [
            UserInterfaceTableRow(["Username", user.username]),
            UserInterfaceTableRow(["Voornaam", user.firstName]),
            UserInterfaceTableRow(["Achternaam", user.lastName]),
            UserInterfaceTableRow(["Registratie datum", user.registration_date]),

            UserInterfaceTableRow(["Rol", "Service Engineer" if user.role == Role.SERVICE_ENGINEER else "Systeem beheerder"])
        ]

        ui = UserInterfaceFlow()
        ui.add(UserInterfaceAlert("Gebruiker " + user.firstName + " " + user.lastName, Color.HEADER))
        ui.add(UserInterfaceTable(rows))
        ui.add(UserInterfacePrompt(
            prompt_text="Druk op W om te wijzigingen of druk D om te verwijderen of druk R om te resetten of druk op "
                        "enter om terug te gaan",
            memory_key="action",
            validations=[OnlyLetterValidation()]
        )
        )

        selection = ui.run()

        selected = selection["action"]

        if selected == "":
            return None

        if selected.upper() == "W":
            if user.role == Role.SERVICE_ENGINEER.name:
                self.update_service_engineer_user(user)
            if user.role == Role.SYSTEM_ADMIN.name:
                self.update_system_admin_user(user)

        elif selected.upper() == "D":
            if user.role == Role.SERVICE_ENGINEER.name:
                self.delete_service_engineer_user(user)
            if user.role == Role.SYSTEM_ADMIN.name:
                self.delete_system_admin_user(user)

        elif selected.upper() == "R":
            if user.role == Role.SERVICE_ENGINEER.name:
                self.reset_service_engineer_user(user)
            if user.role == Role.SYSTEM_ADMIN.name:
                self.reset_system_admin_user(user)

        if user.role == Role.SERVICE_ENGINEER:
            return self.list_service_engineer_users()

        if user.role == Role.SYSTEM_ADMIN:
            return self.list_system_admin_users()

        return None

    @Auth.permission_required(Permission.UserSystemAdminCreate)
    def create_system_admin(self):
        return self.__create_user(Role.SYSTEM_ADMIN)

    @Auth.permission_required(Permission.UserServiceEngineerCreate)
    def create_service_engineer(self):
        return self.__create_user(Role.SERVICE_ENGINEER)

    def __create_user(self, role: Role):

        header = "Service Engineer" if role.SERVICE_ENGINEER else "Systeem beheerder"

        ui = UserInterfaceFlow()
        ui.add(UserInterfaceAlert(text=f"{header} toevoegen", color=Color.HEADER))

        ui = UserForm.get_form(ui, None)

        fields = ui.run()

        user = User()
        user.populate(list(fields.values()), list(fields.keys()))

        plain_pw = UserRepository.generate_valid_password()

        user.password = HashService.hash(plain_pw).decode()

        user.role = role.name

        user.registration_date = datetime.now().strftime("%d-%m-%Y")

        if user.role == Role.SERVICE_ENGINEER.name:
            LogRepository.log(LogType.UserServiceEngineerCreated, f"id: {user.id} username: {user.username}")

        if user.role == Role.SYSTEM_ADMIN.name:
            LogRepository.log(LogType.UserSystemAdminCreated, f"id: {user.id} username: {user.username}")

        UserRepository.persist_user(user)

        IndexService.index_database()

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert("User toegevoegd", Color.OKGREEN),
            2
        )

        pw_ui = UserInterfaceFlow()
        pw_ui.add(UserInterfaceAlert(f"Tijdelijk wachtwoord: {plain_pw}", Color.OKBLUE))
        pw_ui.add(UserInterfacePrompt("Druk op enter om door te gaan", memory_key="action"))
        pw_ui.run()

    @Auth.permission_required(Permission.UserServiceEngineerUpdate)
    def update_service_engineer_user(self, user: User):
        return self.update_user(user)

    @Auth.permission_required(Permission.UserSystemAdminUpdate)
    def update_system_admin_user(self, user: User):
        return self.update_user(user)

    def update_user(self, user: User):
        header = "Service Engineer" if user.role == Role.SERVICE_ENGINEER.name else "Systeem beheerder"

        ui = UserInterfaceFlow()
        ui.add(UserInterfaceAlert(text=header + " " + user.firstName + " " + user.lastName + " wijzigen",
                                  color=Color.HEADER))
        ui.add(UserInterfaceAlert(text=f"Druk op enter om waarde niet te wijzigingen", color=Color.OKCYAN))

        ui = UserForm.get_form(ui, user)

        fields = ui.run()

        user.populate(list(fields.values()), list(fields.keys()))

        UserRepository.update_user(user)

        if user.role == Role.SERVICE_ENGINEER.name:
            LogRepository.log(LogType.UserServiceEngineerUpdated, f"id: {user.id} username: {user.username}")

        if user.role == Role.SYSTEM_ADMIN.name:
            LogRepository.log(LogType.UserSystemAdminUpdated, f"id: {user.id} username: {user.username}")

        IndexService.index_database()

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert("User geüpdatet", Color.OKGREEN),
            2
        )

    @Auth.permission_required(Permission.UserServiceEngineerDelete)
    def delete_service_engineer_user(self, user: User):
        return self.delete_user(user)

    @Auth.permission_required(Permission.UserSystemAdminDelete)
    def delete_system_admin_user(self, user: User):
        return self.delete_user(user)

    def delete_user(self, user: User):
        UserRepository.delete_user(user)

        if user.role == Role.SERVICE_ENGINEER.name:
            LogRepository.log(LogType.UserServiceEngineerDeleted, f"username: {user.username}")

        if user.role == Role.SYSTEM_ADMIN.name:
            LogRepository.log(LogType.UserSystemAdminDeleted, f"username: {user.username}")

        IndexService.index_database()

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert("User verwijderd", Color.OKGREEN),
            2
        )

    @Auth.permission_required(Permission.UserServiceEngineerResetPassword)
    def reset_service_engineer_user(self, user: User):
        return self.reset_password(user)

    @Auth.permission_required(Permission.UserSystemAdminResetPassword)
    def reset_system_admin_user(self, user: User):
        return self.reset_password(user)

    def reset_password(self, user: User):

        plain_pw = UserRepository.generate_valid_password()

        user.password = HashService.hash(plain_pw).decode()

        UserRepository.update_user_password(user)

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert("User gereset", Color.OKGREEN),
            2
        )

        pw_ui = UserInterfaceFlow()
        pw_ui.add(UserInterfaceAlert(f"Tijdelijk wachtwoord: {plain_pw}", Color.OKBLUE))
        pw_ui.add(UserInterfacePrompt("Druk op enter om door te gaan", memory_key="action"))
        pw_ui.run()

    @Auth.permission_required(Permission.UserUpdateOwnPassword)
    def reset_own_password(self):
        user = SecurityHelper.get_logged_in_user()

        ui = UserInterfaceFlow()
        ui.add(UserInterfaceAlert(text="Wachtwoord wijzigen",
                                  color=Color.HEADER))

        ui = UserPasswordForm.get_form(ui)

        fields = ui.run()

        user.password = HashService.hash(fields["password"]).decode()

        UserRepository.update_user_password(user)

        LogRepository.log(LogType.OwnPasswordUpdated)

        IndexService.index_database()

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert("Wachtwoord geüpdatet", Color.OKGREEN),
            2
        )

    @Auth.permission_required(Permission.UserServiceEngineerRead)
    def search_service_engineer_user(self):
        return self.search_users(Role.SERVICE_ENGINEER)

    @Auth.permission_required(Permission.UserSystemAdminRead)
    def search_system_admin_user(self):
        return self.search_users(Role.SYSTEM_ADMIN)

    def search_users(self, role: Role):
        LogRepository.log(LogType.TravellersRead)

        query_ui = UserInterfaceFlow()
        query_ui.add(UserInterfacePrompt(
            prompt_text="Zoeken op naam of username",
            memory_key="query",
            validations=[NoSpecialCharsValidation()]
        )
        )
        query = query_ui.run()['query']

        users = UserRepository.find_by_query(query, role)

        if len(users) == 0:
            UserInterfaceFlow.quick_run(
                UserInterfaceAlert("Geen resultaten gevonden", Color.FAIL),
                2
            )
            if role == Role.SERVICE_ENGINEER:
                return self.list_service_engineer_users()
            if role == Role.SYSTEM_ADMIN:
                return self.list_system_admin_users()

        if role == Role.SERVICE_ENGINEER:
            return self.list_service_engineer_users(users)
        if role == Role.SYSTEM_ADMIN:
            return self.list_system_admin_users(users)

        return None
