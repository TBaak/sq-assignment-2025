from Controllers.BackupController import BackupController
from Controllers.LogController import LogController
from Controllers.ScooterController import ScooterController
from Controllers.TravellerController import TravellerController
from Controllers.UserController import UserController
from DTO.MenuOption import MenuOption
from Enum.Color import Color
from Security.AuthorizationService import AuthorizationService
from Security.Enum.Permission import Permission
from View.UserInterfaceAlert import UserInterfaceAlert
from View.UserInterfaceFlow import UserInterfaceFlow
from View.UserInterfacePrompt import UserInterfacePrompt
from View.UserInterfaceTable import UserInterfaceTable
from View.UserInterfaceTableRow import UserInterfaceTableRow


class MenuController:
    menu_choices: list[MenuOption] = []

    def __init__(self):
        self.__create_menu_options()

    # Once called this will never terminate.
    # So if another controller action is finished it will return to this menu.
    def menu(self) -> None:
        menu_ui = UserInterfaceFlow()
        menu_ui.add(UserInterfaceAlert("Menu", Color.HEADER))  # Header

        rows = list(map(lambda c: [c.name], self.menu_choices))
        rows = UserInterfaceTable.add_row_numbers(rows)
        table_rows = list(map(lambda m_row: UserInterfaceTableRow(m_row), rows))

        menu_ui.add(UserInterfaceTable(rows=table_rows, has_header=False))
        menu_ui.add(UserInterfacePrompt("Kies een optie of druk op ENTER om af te sluiten", "selection"))

        while True:
            menu_result = menu_ui.run()

            if menu_result["selection"] == "":
                break

            try:
                int(menu_result["selection"])
                self.menu_choices[int(menu_result["selection"]) - 1].action()
            except IndexError:
                UserInterfaceFlow.quick_run(
                    UserInterfaceAlert("Ongeldige keuze", Color.FAIL),
                    1
                )
                continue

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert("Tot ziens!", Color.HEADER)
        )

    def user_type_menu(self) -> None:

        uc = UserController()

        if AuthorizationService.current_user_has_permission(Permission.UserServiceEngineerRead) \
                and not AuthorizationService.current_user_has_permission(Permission.UserSystemAdminRead):
            return uc.list_service_engineer_users()

        if not AuthorizationService.current_user_has_permission(Permission.UserServiceEngineerRead) \
                and AuthorizationService.current_user_has_permission(Permission.UserSystemAdminRead):
            return uc.list_system_admin_users()

        menu_ui = UserInterfaceFlow()
        menu_ui.add(UserInterfaceAlert("Welke type user wilt u bekijken?", Color.HEADER))

        rows = [
            ["Service Engineers"],
            ["Systeem beheerders"]
        ]

        rows = UserInterfaceTable.add_row_numbers(rows)

        table_rows = list(map(lambda m_row: UserInterfaceTableRow(m_row), rows))

        menu_ui.add(UserInterfaceTable(rows=table_rows, has_header=False))
        menu_ui.add(UserInterfacePrompt("Kies een optie", "selection"))

        menu_result = menu_ui.run()

        if menu_result["selection"] == "1":
            return uc.list_service_engineer_users()

        if menu_result["selection"] == "2":
            return uc.list_system_admin_users()

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert("Ongeldige keuze", Color.FAIL),
            1
        )

        mc = MenuController()
        return mc.user_type_menu()

    def user_create_type_menu(self) -> None:

        uc = UserController()

        if AuthorizationService.current_user_has_permission(Permission.UserServiceEngineerRead) \
                and not AuthorizationService.current_user_has_permission(Permission.UserSystemAdminRead):
            return uc.create_service_engineer()

        if not AuthorizationService.current_user_has_permission(Permission.UserServiceEngineerRead) \
                and AuthorizationService.current_user_has_permission(Permission.UserSystemAdminRead):
            return uc.create_system_admin()

        menu_ui = UserInterfaceFlow()
        menu_ui.add(UserInterfaceAlert("Welke type user wilt u toevoegen?", Color.HEADER))

        rows = [
            ["Service Engineers"],
            ["Systeem beheerders"]
        ]

        rows = UserInterfaceTable.add_row_numbers(rows)

        table_rows = list(map(lambda m_row: UserInterfaceTableRow(m_row), rows))

        menu_ui.add(UserInterfaceTable(rows=table_rows, has_header=False))
        menu_ui.add(UserInterfacePrompt("Kies een optie", "selection"))

        menu_result = menu_ui.run()

        if menu_result["selection"] == "1":
            return uc.create_service_engineer()

        if menu_result["selection"] == "2":
            return uc.create_system_admin()

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert("Ongeldige keuze", Color.FAIL),
            1
        )

        mc = MenuController()
        return mc.user_type_menu()

    def __create_menu_options(self):

        tc = TravellerController()

        if AuthorizationService.current_user_has_permission(Permission.TravellerRead):
            self.menu_choices.append(MenuOption("Traveller overzicht", tc.list_travellers))

        if AuthorizationService.current_user_has_permission(Permission.TravellerCreate):
            self.menu_choices.append(MenuOption("Traveller toevoegen", tc.add_traveller))

        sc = ScooterController()

        if AuthorizationService.current_user_has_permission(Permission.ScooterRead):
            self.menu_choices.append(MenuOption("Scooter overzicht", sc.list_scooters))

        if AuthorizationService.current_user_has_permission(Permission.ScooterCreate):
            self.menu_choices.append(MenuOption("Scooter toevoegen", sc.add_scooter))

        lc = LogController()

        if AuthorizationService.current_user_has_permission(Permission.LogRead):
            self.menu_choices.append(MenuOption("Logs bekijken", lc.list_logs))

        if AuthorizationService.current_user_has_permission(Permission.UserServiceEngineerRead) \
                or AuthorizationService.current_user_has_permission(Permission.UserSystemAdminRead):
            self.menu_choices.append(MenuOption("User overzicht", self.user_type_menu))

        if AuthorizationService.current_user_has_permission(Permission.UserServiceEngineerRead) \
                or AuthorizationService.current_user_has_permission(Permission.UserSystemAdminRead):
            self.menu_choices.append(MenuOption("User aanmaken", self.user_create_type_menu))

        bc = BackupController()

        if AuthorizationService.current_user_has_permission(Permission.BackupCreate):
            self.menu_choices.append(MenuOption("Backup maken", bc.create_backup))

        if AuthorizationService.current_user_has_permission(Permission.BackupRestore):
            self.menu_choices.append(MenuOption("Backup terugzetten", bc.list_backups))

        uc = UserController()

        if AuthorizationService.current_user_has_permission(Permission.UserUpdateOwnPassword):
            self.menu_choices.append(MenuOption("Wachtwoord wijzigingen", uc.reset_own_password))
