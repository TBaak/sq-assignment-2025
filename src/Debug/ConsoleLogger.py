class ConsoleLogger(object):

    loglevel = 0

    @staticmethod
    def set_loglevel(level: int):
        ConsoleLogger.loglevel = level

    @staticmethod
    def v(message: str):
        if ConsoleLogger.loglevel >= 1:
            print(f"{message}")

    @staticmethod
    def vv(message: str):
        if ConsoleLogger.loglevel >= 2:
            print(f"{message}")

    @staticmethod
    def vvv(message: str):
        if ConsoleLogger.loglevel >= 3:
            print(f"{message}")