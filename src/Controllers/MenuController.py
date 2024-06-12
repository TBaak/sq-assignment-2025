from Controllers.MemberController import MemberController
from DTO.MenuOption import MenuOption
from Enum.Color import Color
from View.UserInterfaceAlert import UserInterfaceAlert
from View.UserInterfaceFlow import UserInterfaceFlow
from View.UserInterfacePrompt import UserInterfacePrompt
from View.UserInterfaceTable import UserInterfaceTable
from View.UserInterfaceTableRow import UserInterfaceTableRow


class MenuController:

    def __init__(self):
        mc = MemberController()

        self.menu_choices = [
            MenuOption("Member overzicht", mc.list_members),
            MenuOption("Member toevoegen", mc.add_member),
        ]

    # Once called this will never terminate.
    # So if another controller action is finished it will return to this menu.
    def menu(self) -> None:
        menu_ui = UserInterfaceFlow()
        menu_ui.add(UserInterfaceAlert("Menu", Color.OKCYAN))  # Header

        rows = list(map(lambda c: [c.name], self.menu_choices))
        rows = UserInterfaceTable.add_row_numbers(rows)
        table_rows = list(map(lambda m_row: UserInterfaceTableRow(m_row), rows))

        menu_ui.add(UserInterfaceTable(rows=table_rows, has_header=False))
        menu_ui.add(UserInterfacePrompt("Kies een optie", "selection"))

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