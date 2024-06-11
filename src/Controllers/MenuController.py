from Controllers.MemberController import MemberController
from DTO.MenuOption import MenuOption
from Enum.Color import Color
from View.UserInterfaceAlert import UserInterfaceAlert
from View.UserInterfaceFlow import UserInterfaceFlow
from View.UserInterfacePrompt import UserInterfacePrompt

class MenuController:

    def __init__(self):
        mc = MemberController()

        self.menu_choices = [
            MenuOption("Member toevoegen", mc.add_member),
        ]

    # Once called this will never terminate.
    # So if another controller action is finished it will return to this menu.
    def menu(self) -> None:
        menu_ui = UserInterfaceFlow()
        menu_ui.add(UserInterfaceAlert("Menu", Color.OKCYAN))  # Header

        for index, choice in enumerate(self.menu_choices):
            extra_room = "  - " if len(str(index + 1)) == 1 else " - "
            menu_ui.add(UserInterfaceAlert(str(index + 1) + extra_room + choice.name, Color.WHITE))

        menu_ui.add(UserInterfacePrompt("Kies een optie: ", "selection"))

        while True:
            menu_result = menu_ui.run()

            try:
                int(menu_result["selection"])
                self.menu_choices[int(menu_result["selection"]) - 1].action()
                break
            except:
                UserInterfaceFlow.quick_run(
                    UserInterfaceAlert("Ongeldige keuze", Color.FAIL),
                    1
                )
                continue