from Enum.Color import Color
from Enum.LogType import LogType
from Enum.UserType import UserType
from Form.UserForm import UserForm
from Models.User import User
from Repository.LogRepository import LogRepository
from Repository.UserRepository import UserRepository
from Security.AuthorizationDecorator import Auth
from Security.Enum.Permission import Permission
from Security.Enum.Role import Role
from Service.HashService import HashService
from Service.IndexService import IndexService
from View.UserInterfaceAlert import UserInterfaceAlert
from View.UserInterfaceFlow import UserInterfaceFlow
from View.UserInterfacePrompt import UserInterfacePrompt
from View.UserInterfaceTable import UserInterfaceTable
from View.UserInterfaceTableRow import UserInterfaceTableRow
from View.Validations.OnlyLetterValdation import OnlyLetterValidation


class UserController:

    @Auth.permission_required(Permission.UserConsultantRead)
    def list_consultant_users(self, users: list[User] = None):

        UserInterfaceFlow.quick_run_till_next(
            UserInterfaceAlert("Consultant overzicht aan het laden...", Color.HEADER)
        )

        LogRepository.log(LogType.UserConsultantRead)

        self.__show_users(Role.CONSULTANT, users)

    @Auth.permission_required(Permission.UserSystemAdminRead)
    def list_system_admin_users(self, users: list[User] = None):

        UserInterfaceFlow.quick_run_till_next(
            UserInterfaceAlert("Systeem beheerder overzicht aan het laden...", Color.HEADER)
        )

        LogRepository.log(LogType.UserSystemAdminRead)

        self.__show_users(Role.SYSTEM_ADMIN, users)

    def __show_users(self, role: Role, users: list[User] = None):

        header_type = "Consultant" if role.CONSULTANT else "Systeem beheerder"
        header = f"{header_type} overzicht" if users is None else "Zoekresultaten"

        if users is None:
            users = UserRepository.find_all_by_role(role)

        rows = map(lambda u: [u.username, u.firstName, u.lastName, u.registrationDate], users)
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
            print("implement this")
            exit(0)

        user_index = int(selected) - 1  # TODO: Handle out of bounds

        selected_user = users[user_index]

        if role == Role.SYSTEM_ADMIN:
            self.show_system_admin_user(selected_user)

        if role == Role.CONSULTANT:
            self.show_system_admin_user(selected_user)

        # TODO no role?

        return self.__show_users(role, users)

    @Auth.permission_required(Permission.UserConsultantRead)
    def show_consultant_user(self, user: User):

        LogRepository.log(LogType.MemberRead)

        return self.__show_user(user)

    @Auth.permission_required(Permission.UserSystemAdminRead)
    def show_system_admin_user(self, user: User):

        LogRepository.log(LogType.MemberRead)

        return self.__show_user(user)

    def __show_user(self, user: User):

        rows = [
            UserInterfaceTableRow(["Username", user.username]),
            UserInterfaceTableRow(["Voornaam", user.firstName]),
            UserInterfaceTableRow(["Achternaam", user.lastName]),
            UserInterfaceTableRow(["Registratie datum", user.registrationDate]),

            UserInterfaceTableRow(["Rol", "Consultant" if user.role == Role.CONSULTANT else "Systeem beheerder"])
        ]

        ui = UserInterfaceFlow()
        ui.add(UserInterfaceAlert("Gebruiker " + user.firstName + " " + user.lastName, Color.HEADER))
        ui.add(UserInterfaceTable(rows))
        ui.add(UserInterfacePrompt(
            prompt_text="Druk op W om te wijzigingen of druk D om te verwijderen of druk op enter om terug te gaan",
            memory_key="action",
            validations=[OnlyLetterValidation()]
        )
        )

        selection = ui.run()

        selected = selection["action"]

        if selected == "":
            return

        if selected.upper() == "W":
            pass
            # self.update_member(member)

        elif selected.upper() == "D":
            pass
            # self.delete_member(member)

        if user.role == Role.CONSULTANT:
            self.list_consultant_users()

        if user.role == Role.SYSTEM_ADMIN:
            self.list_system_admin_users()

    @Auth.permission_required(Permission.UserSystemAdminCreate)
    def create_system_admin(self):
        return self.__create_user(Role.SYSTEM_ADMIN)

    def __create_user(self, role: Role):

        header = "Consultant" if role.CONSULTANT else "Systeem beheerder"

        ui = UserInterfaceFlow()
        ui.add(UserInterfaceAlert(text=f"{header} toevoegen", color=Color.HEADER))

        ui = UserForm.get_form(ui, None)

        fields = ui.run()

        user = User()
        user.populate(list(fields.values()), list(fields.keys()))

        plain_pw = UserRepository.generate_valid_password()

        user.password = HashService.hash(plain_pw)

        user.role = role.name

        LogRepository.log(LogType.MemberCreated, f"id: {user.id} username: {user.username}")

        UserRepository.persist_user(user)

        IndexService.index_database()

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert("User toegevoegd", Color.OKGREEN),
            2
        )

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert(f"Tijdelijk wachtwoord: {plain_pw}", Color.OKGREEN),
            2
        )
