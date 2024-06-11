import sys

from Configuration.DatabaseConfiguration import DatabaseConfiguration
from Configuration.DatabaseSeeder import DatabaseSeeder
from Controllers.LoginController import LoginController
from Debug.ConsoleLogger import ConsoleLogger
from Enum.Color import Color
from Service.EncryptionService import EncryptionService
from Service.IndexService import IndexService
from Test.CreateAdminTest import CreateAdminTest
from Test.CreateMemberTest import CreateMemberTest
from View.UserInterfaceAlert import UserInterfaceAlert
from View.UserInterfaceFlow import UserInterfaceFlow


def main():

    UserInterfaceFlow.quick_run(UserInterfaceAlert("-= Welkom in het User Management systeem van Unique Meal =-", Color.HEADER), 1)

    UserInterfaceFlow.quick_run(UserInterfaceAlert("[ ] Keys initialiseren..."), 1)

    EncryptionService.create_certificates_if_not_exist()

    UserInterfaceFlow.quick_run(UserInterfaceAlert("[+] Keys geïnitialiseerd", Color.OKGREEN), 1)

    UserInterfaceFlow.quick_run(UserInterfaceAlert("[ ] Database initialiseren..."), 1)

    DatabaseConfiguration.start()
    DatabaseSeeder.seed()

    UserInterfaceFlow.quick_run(UserInterfaceAlert("[+] Database geïnitialiseerd ", Color.OKGREEN), 1)

    UserInterfaceFlow.quick_run(UserInterfaceAlert("[ ] Database indexeren..."), 1)

    IndexService.index_database()

    UserInterfaceFlow.quick_run(UserInterfaceAlert("[+] Database geïndexeerd ", Color.OKGREEN), 1)

    # CreateMemberTest.run()
    # CreateAdminTest.run(uname="super_admin", pword="Admin_123?")
    # exit(0)

    lc = LoginController()
    lc.login()


if __name__ == '__main__':

    # DEBUG CONSOLE LOGGING
    if len(sys.argv) > 1:
        match sys.argv[1].lower():
            case "-v":
                ConsoleLogger.set_loglevel(1)
            case "-vv":
                ConsoleLogger.set_loglevel(2)
            case "-vvv":
                ConsoleLogger.set_loglevel(3)

    main()
