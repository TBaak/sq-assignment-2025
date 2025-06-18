from Enum.Color import Color
from Repository.LogRepository import LogRepository
from Security.AuthorizationDecorator import Auth
from Security.Enum.Permission import Permission
from View.UserInterfaceAlert import UserInterfaceAlert
from View.UserInterfaceFlow import UserInterfaceFlow
from View.UserInterfacePrompt import UserInterfacePrompt
from View.UserInterfaceTable import UserInterfaceTable
from View.UserInterfaceTableRow import UserInterfaceTableRow


class LogController:

    @Auth.permission_required(Permission.LogRead)
    def list_logs(self):

        logs = LogRepository.find_all()

        rows = map(lambda l: l.split(','), logs)

        rows = list(map(lambda l_row: UserInterfaceTableRow(l_row), rows))

        rows.insert(0, UserInterfaceTableRow(
            ["#", "Datum", "Tijd", "Username", "Activiteit", "Extra informatie", "Verdachte activiteit"]))

        ui = UserInterfaceFlow()
        ui.add(UserInterfaceAlert("Logs", Color.HEADER))
        ui.add(UserInterfaceTable(rows=rows, has_header=True))
        ui.add(UserInterfacePrompt(
            prompt_text="Druk op ENTER om terug te gaan",
            validations=[]
        )
        )

        ui.run()