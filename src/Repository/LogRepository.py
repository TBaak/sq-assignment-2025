import base64
from datetime import datetime

from Debug.ConsoleLogger import ConsoleLogger
from Enum.LogType import LogType
from Security.SecurityHelper import SecurityHelper
from Service.EncryptionService import EncryptionService


class LogRepository:
    # TODO: OWASP logging?

    logFilename = "log.csv"

    @staticmethod
    def log(log_type: LogType, additional_message: str = ""):
        log_file = open(LogRepository.logFilename, "a")

        count = LogRepository.__get_log_length()

        date = datetime.now().strftime("%d-%m-%Y")
        time = datetime.now().strftime("%H:%M:%S")

        username = SecurityHelper.get_logged_in_user().username \
            if SecurityHelper.get_logged_in_user() is not None else "---"

        suspicous = "Ja" if log_type.value.suspicious else "Nee"

        log_line = f"{count + 1},{date},{time},{username},{log_type.value.message},{additional_message},{suspicous}"

        ConsoleLogger.v(log_line)

        log_line_encrypted = EncryptionService.encrypt(log_line)

        log_file.write(base64.b64encode(log_line_encrypted).decode('utf-8') + "\n")
        log_file.close()

    @staticmethod
    def find_all() -> list[str]:
        log_file = open(LogRepository.logFilename, "r") # TODO: Handle not exist

        logs = []

        for line in log_file:
            logs.append(EncryptionService.decrypt(base64.b64decode(line)))

        log_file.close()

        return logs

    @staticmethod
    def __get_log_length() -> int:
        log_file = open(LogRepository.logFilename, "r")

        count = 0
        for count, line in enumerate(log_file):
            pass

        log_file.close()

        return count
