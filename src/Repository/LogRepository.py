import base64
import os
from datetime import datetime

from Enum.Color import Color
from Enum.LogType import LogType
from Security.SecurityHelper import SecurityHelper
from Service.EncryptionService import EncryptionService
from View.UserInterfaceAlert import UserInterfaceAlert
from View.UserInterfaceFlow import UserInterfaceFlow


class LogRepository:
    # TODO: OWASP logging?

    log_filename = "log.csv"
    log_dir = "../../Storage"

    @staticmethod
    def log(log_type: LogType, additional_message: str = ""):

        base_dir = LogRepository.__check_log_dir()

        log_path = os.path.realpath(base_dir + LogRepository.log_dir + "/" + LogRepository.log_filename)

        log_file = open(log_path, "a+")

        count = LogRepository.__get_log_length()

        date = datetime.now().strftime("%d-%m-%Y")
        time = datetime.now().strftime("%H:%M:%S")

        username = SecurityHelper.get_logged_in_user().username \
            if SecurityHelper.get_logged_in_user() is not None else "---"

        suspicous = "Ja" if log_type.value.suspicious else "Nee"

        log_line = f"{count + 1},{date},{time},{username},{log_type.value.message},{additional_message},{suspicous}"


        log_line_encrypted = EncryptionService.encrypt(log_line)

        log_file.write(base64.b64encode(log_line_encrypted.encode()).decode('utf-8') + "\n")
        log_file.close()

    @staticmethod
    def find_all() -> list[str]:
        base_dir = LogRepository.__check_log_dir()

        log_path = os.path.realpath(base_dir + LogRepository.log_dir + "/" + LogRepository.log_filename)

        log_file = open(log_path, "r+")

        logs = []

        for line in log_file:
            logs.append(EncryptionService.decrypt(base64.b64decode(line).decode()))

        log_file.close()

        return logs

    @staticmethod
    def __get_log_length() -> int:
        base_dir = LogRepository.__check_log_dir()

        log_path = os.path.realpath(base_dir + LogRepository.log_dir + "/" + LogRepository.log_filename)

        log_file = open(log_path, "r")

        count = 0
        for count, line in enumerate(log_file):
            pass

        log_file.close()

        return count



    @staticmethod
    def __check_log_dir():
        base_dir = os.path.dirname(os.path.realpath(__file__))
        if not os.path.exists(os.path.realpath(base_dir + LogRepository.log_dir)):
            UserInterfaceFlow.quick_run(
                UserInterfaceAlert("Log opslag fout, afsluiten...", Color.FAIL),
                1
            )
            exit(1)
        return base_dir
