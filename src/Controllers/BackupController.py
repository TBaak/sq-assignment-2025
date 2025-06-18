import os
import shutil
import string
from datetime import datetime
import random

from Enum.Color import Color
from Enum.LogType import LogType
from Models.BackupOneTimeCode import BackupOneTimeCode
from Repository.BackupOneTimeCodeRepository import BackupOneTimeCodeRepository
from Repository.BaseClasses.DBRepository import DBRepository
from Repository.LogRepository import LogRepository
from Repository.UserRepository import UserRepository
from Security.AuthorizationDecorator import Auth
from Security.Enum.Permission import Permission
from Security.Enum.Role import Role
from View.UserInterfaceAlert import UserInterfaceAlert
from View.UserInterfaceFlow import UserInterfaceFlow
from View.UserInterfacePrompt import UserInterfacePrompt
from View.UserInterfaceTable import UserInterfaceTable
from View.UserInterfaceTableRow import UserInterfaceTableRow
from View.Validations.LengthValidation import LengthValidation
from View.Validations.NotBlankValidation import NotBlankValidation
from View.Validations.OnlyLetterValidation import OnlyLetterValidation


class BackupController:

    bk_dir = "/../Storage/Backups"
    storage_dir = "/../Storage"

    @Auth.permission_required(Permission.BackupRestore)
    def list_backups(self):
        base_dir = os.path.dirname(os.path.realpath(__file__))
        backup_dir = os.path.realpath(base_dir + BackupController.bk_dir)

        if not os.path.exists(backup_dir):
            UserInterfaceFlow.quick_run(
                UserInterfaceAlert("Er zijn geen backups beschikbaar", Color.WARNING),
                2
            )
            return

        backup_files = os.listdir(backup_dir)

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
        except (ValueError, IndexError):
            UserInterfaceFlow.quick_run(
                UserInterfaceAlert("Ongeldige keuze", Color.FAIL),
                1
            )
            return

    def __restore_backup(self, selected_backup):
        base_dir = os.path.dirname(os.path.realpath(__file__))
        backup_dir = os.path.realpath(base_dir + BackupController.bk_dir)

        selected_backup_dir = os.path.realpath(f"{backup_dir}/{selected_backup}")

        if not os.path.exists(backup_dir) or not os.path.exists(selected_backup_dir):
            UserInterfaceFlow.quick_run(
                UserInterfaceAlert("Backup niet gevonden", Color.FAIL),
                2
            )
            return

        backup_upzipped_name = selected_backup.split(".")[0]

        backup_upzipped_dir = os.path.realpath(f"{backup_dir}/{backup_upzipped_name}")

        shutil.unpack_archive(selected_backup_dir, backup_upzipped_dir)

        db_file = os.path.realpath(f"{base_dir}/{BackupController.storage_dir}/{DBRepository.db_filename}")

        shutil.copy(f"{backup_upzipped_dir}/{DBRepository.db_filename}", db_file)

        shutil.rmtree(backup_upzipped_dir)

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
        base_dir = os.path.dirname(os.path.realpath(__file__))
        backup_dir = os.path.realpath(base_dir + BackupController.bk_dir)

        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        db_file = os.path.realpath(f"{base_dir}/{BackupController.storage_dir}/{DBRepository.db_filename}")
        # log_file = os.path.realpath(f"{base_dir}/{BackupController.storage_dir}/{LogRepository.log_filename}")

        backup_filename = f"backup_{datetime.now().strftime("%H_%M_%S_%d-%m-%Y")}"

        backup_folder = os.path.realpath(f"{backup_dir}/{backup_filename}")

        zip_folder = os.path.realpath(f"{backup_dir}/{backup_filename}")

        os.mkdir(backup_folder)

        # shutil.copy(log_file, f"{backup_folder}/{LogRepository.log_filename}")

        db_copied_file = os.path.realpath(f"{backup_folder}/{DBRepository.db_filename}")

        shutil.copy(db_file, db_copied_file)

        # Remove table from the copied database file

        try:
            db = DBRepository.create_connection(db_copied_file, False)
        except Exception as e:
            UserInterfaceFlow.quick_run(
                UserInterfaceAlert("Fout bij het maken van de backup, database niet aanpassen", Color.FAIL),
                2
            )
            return

        cursor = db.cursor()
        cursor.execute("DROP TABLE IF EXISTS backup_one_time_codes;")
        db.commit()
        cursor.close()
        db.close()

        shutil.make_archive(f"{backup_folder}", 'zip', backup_folder)

        shutil.move(f"{backup_folder}.zip", f"{zip_folder}.zip")

        shutil.rmtree(backup_folder)

        LogRepository.log(LogType.BackupCreated, f"Backup created: {backup_folder}.zip")

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert(f"Backup gemaakt: {backup_folder}.zip", Color.OKGREEN),
            2
        )

    @Auth.permission_required(Permission.BackupRestoreWithOtc)
    def restore_with_otc(self):

        ui = UserInterfaceFlow()
        ui.add(UserInterfaceAlert("Backups", Color.HEADER))  # Header
        ui.add(UserInterfaceAlert("Na het terugzetten van een backup word u uitgelogd", Color.WARNING))

        ui.add(UserInterfacePrompt("Voer de one-time-code in", "otc",
                                   validations=[NotBlankValidation(), LengthValidation(length=32), OnlyLetterValidation()]))

        result = ui.run()

        otc_code = result["otc"]

        otc_res = BackupOneTimeCodeRepository.find_by_code(otc_code)

        otc = otc_res[0]

        if otc is None:
            UserInterfaceFlow.quick_run(
                UserInterfaceAlert("One-time-code niet gevonden of ongeldig", Color.FAIL),
                2
            )
            return

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert(f"Backup wordt hersteld...", Color.OKBLUE),
            2
        )

        backup_name = otc.backup_name

        self.__restore_backup(backup_name)

    @Auth.permission_required(Permission.BackupCreateOtc)
    def create_otc(self):
        base_dir = os.path.dirname(os.path.realpath(__file__))
        backup_dir = os.path.realpath(base_dir + BackupController.bk_dir)

        if not os.path.exists(backup_dir):
            UserInterfaceFlow.quick_run(
                UserInterfaceAlert("Er zijn geen backups beschikbaar", Color.WARNING),
                2
            )
            return

        backup_files = os.listdir(backup_dir)

        users = UserRepository.find_all_by_role(Role.SYSTEM_ADMIN)

        if len(users) == 0:
            UserInterfaceFlow.quick_run(
                UserInterfaceAlert("Er zijn geen Systeem beheerders beschikbaar", Color.WARNING),
                2
            )
            return

        rows = map(lambda u: [u.username, u.first_name, u.last_name, u.registration_date], users)
        rows = list(rows)

        rows = UserInterfaceTable.add_row_numbers(rows)

        rows = list(map(lambda m_row: UserInterfaceTableRow(m_row), rows))

        rows.insert(0, UserInterfaceTableRow(
            ["#", "Username", "Voornaam", "Achternaam", "Registratie datum"]))

        ui = UserInterfaceFlow()
        ui.add(UserInterfaceAlert("Backup one-time-code", Color.HEADER))
        ui.add(UserInterfaceTable(rows=rows, has_header=True))
        ui.add(UserInterfacePrompt(
            prompt_text="Geef het nummer om te bekijken of druk op ENTER om terug te gaan",
            memory_key="action"
        )
        )
        selection = ui.run()

        selected = selection["action"]

        if selected == "":
            return

        try:
            selected_user = users[int(selected) - 1]
        except Exception as e:
            UserInterfaceFlow.quick_run(
                UserInterfaceAlert("Ongeldige keuze", Color.FAIL),
                1
            )
            return

        bk_ui = UserInterfaceFlow()
        bk_ui.add(UserInterfaceAlert("Backups", Color.HEADER))  # Header

        rows = list(map(lambda b: [b], backup_files))
        rows = UserInterfaceTable.add_row_numbers(rows)
        table_rows = list(map(lambda m_row: UserInterfaceTableRow(m_row), rows))

        table_rows.insert(0, UserInterfaceTableRow(
            ["#", "Backup bestand"]))

        bk_ui.add(UserInterfaceTable(rows=table_rows, has_header=True))
        bk_ui.add(UserInterfacePrompt("Kies een backup om een one-time-code aan te maken of druk op ENTER om terug te gaan",
                                   "selection"))

        result = bk_ui.run()

        if result["selection"] == "":
            return

        try:
            selected_backup = backup_files[int(result["selection"]) - 1]
        except (ValueError, IndexError):
            UserInterfaceFlow.quick_run(
                UserInterfaceAlert("Ongeldige keuze", Color.FAIL),
                1
            )
            return

        code = self.generate_otc_code()

        backup_one_time_code = BackupOneTimeCode()
        backup_one_time_code.populate(
            [code, selected_backup, selected_user.id],
            ["one_time_code", "backup_name", "user_id"])

        BackupOneTimeCodeRepository.persist_otc(backup_one_time_code)

        LogRepository.log(LogType.BackupOneTimeCodeCreated, f"One-time-code created for backup: {selected_backup} for user: {selected_user.username}")

        code_ui = UserInterfaceFlow()
        code_ui.add(UserInterfaceAlert(f"One-time-code: {code}", Color.OKBLUE))
        code_ui.add(UserInterfacePrompt("Druk op enter om door te gaan"))
        code_ui.run()

    @Auth.permission_required(Permission.BackupCreateOtc)
    def list_otc(self):
        otc_list = BackupOneTimeCodeRepository.find_all()

        ui = UserInterfaceFlow()
        ui.add(UserInterfaceAlert("One-time-codes", Color.HEADER))

        otc_list = list(filter(lambda otc: otc.getUser() is not None, otc_list))

        rows = map(lambda otc: [otc.getUser().username, otc.backup_name, otc.one_time_code], otc_list)
        rows = list(rows)
        rows = UserInterfaceTable.add_row_numbers(rows)
        rows = list(map(lambda m_row: UserInterfaceTableRow(m_row), rows))
        rows.insert(0, UserInterfaceTableRow(
            ["#", "Username", "Back-up", "One-time-code"]))

        ui = UserInterfaceFlow()
        ui.add(UserInterfaceAlert("Backup one-time-code", Color.HEADER))
        ui.add(UserInterfaceTable(rows=rows, has_header=True))
        ui.add(UserInterfacePrompt(
            prompt_text="Geef het nummer om code in te trekken of druk op ENTER om terug te gaan",
            memory_key="action"
        ))
        selection = ui.run()

        selected = selection["action"]

        if selected == "":
            return

        try:
            selected_otc = otc_list[int(selected) - 1]
        except (ValueError, IndexError):
            UserInterfaceFlow.quick_run(
                UserInterfaceAlert("Ongeldige keuze", Color.FAIL),
                1
            )
            return

        BackupOneTimeCodeRepository.delete_otc(selected_otc)

        LogRepository.log(LogType.BackupOneTimeCodeDeleted,
                          f"One-time-code deleted for backup: {selected_otc.backup_name} for user: {selected_otc.getUser().username}")

        UserInterfaceFlow.quick_run(
            UserInterfaceAlert(f"One-time-code voor backup: {selected_otc.backup_name} is ingetrokken", Color.OKBLUE),
            2
        )

        return


    @staticmethod
    def generate_otc_code() -> str:
        uppercase = string.ascii_uppercase
        return ''.join(random.choice(uppercase) for _ in range(32))



