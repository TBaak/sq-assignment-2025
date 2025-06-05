import os
import shutil
from datetime import datetime

from Enum.Color import Color
from Enum.LogType import LogType
from Repository.BaseClasses.DBRepository import DBRepository
from Repository.LogRepository import LogRepository
from Security.AuthorizationDecorator import Auth
from Security.Enum.Permission import Permission
from View.UserInterfaceAlert import UserInterfaceAlert
from View.UserInterfaceFlow import UserInterfaceFlow
from View.UserInterfacePrompt import UserInterfacePrompt
from View.UserInterfaceTable import UserInterfaceTable
from View.UserInterfaceTableRow import UserInterfaceTableRow


class BackupController:

    @Auth.permission_required(Permission.BackupRestore)
    def list_backups(self):
        # Read all files in the backup folder
        backup_files = os.listdir("Backups")

        ui = UserInterfaceFlow()
        ui.add(UserInterfaceAlert("Backups", Color.HEADER))  # Header
        ui.add(UserInterfaceAlert("Na het terugzetten van een backup word u uitgelogd", Color.WARNING))  # Header

        rows = list(map(lambda b: [b], backup_files))
        rows = UserInterfaceTable.add_row_numbers(rows)
        table_rows = list(map(lambda m_row: UserInterfaceTableRow(m_row), rows))

        table_rows.insert(0, UserInterfaceTableRow(
            ["#", "Backup bestand"]))

        ui.add(UserInterfaceTable(rows=table_rows, has_header=True))
        ui.add(UserInterfacePrompt("Kies een backup om deze terug te zetten of druk op ENTER om terug te gaan", "selection"))

        result = ui.run()

        if result["selection"] == "":
            return

        try:
            selected = int(result["selection"]) - 1
            selected_backup = backup_files[selected]
            self.__restore_backup(selected_backup)
        except IndexError:
            UserInterfaceFlow.quick_run(
                UserInterfaceAlert("Ongeldige keuze", Color.FAIL),
                1
            )
            return

    def __restore_backup(self, selected_backup):
        backup_folder = selected_backup.split(".")[0]
        shutil.unpack_archive(f"Backups/{selected_backup}", backup_folder)

        db_file = DBRepository.db_filename
        log_file = LogRepository.log_filename

        shutil.copy(f"{backup_folder}/{log_file}", log_file)
        shutil.copy(f"{backup_folder}/{db_file}", db_file)

        shutil.rmtree(backup_folder)

        LogRepository.log(LogType.BackupRestored, f"Backup restored: {selected_backup}")

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert(f"Backup terug gezet", Color.OKGREEN),
            2
        )

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert(f"U word uitgelogd", Color.OKBLUE),
            2
        )

        exit(0)

    @Auth.permission_required(Permission.BackupCreate)
    def create_backup(self):
        db_file = DBRepository.db_filename
        log_file = LogRepository.log_filename

        backup_folder = "backup_" + datetime.now().strftime("%H.%M.%S_%d-%m-%Y")

        os.mkdir(backup_folder)

        shutil.copy(log_file, f"{backup_folder}/{log_file}")
        shutil.copy(db_file, f"{backup_folder}/{db_file}")

        shutil.make_archive(f"{backup_folder}", 'zip', backup_folder)

        shutil.move(f"{backup_folder}.zip", f"Backups/{backup_folder}.zip")

        shutil.rmtree(backup_folder)

        LogRepository.log(LogType.BackupCreated, f"Backup created: {backup_folder}.zip")

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert(f"Backup created: {backup_folder}.zip", Color.OKGREEN),
            2
        )



