import sys

from Configuration.DatabaseConfiguration import DatabaseConfiguration
from Configuration.DatabaseSeeder import DatabaseSeeder
from Controllers.LoginController import LoginController
from Enum.Color import Color
from Service.EncryptionService import EncryptionService
from Service.IndexService import IndexService
from View.UserInterfaceAlert import UserInterfaceAlert
from View.UserInterfaceFlow import UserInterfaceFlow


def main():
    UserInterfaceFlow.quick_run(UserInterfaceAlert("-= Welkom in het management systeem van Urban Mobility =-", Color.HEADER), 1)

    UserInterfaceFlow.quick_run(UserInterfaceAlert("[ ] Database initialiseren..."), 0)

    DatabaseConfiguration.start()

    UserInterfaceFlow.quick_run(UserInterfaceAlert("[+] Database geïnitialiseerd ", Color.OKGREEN), 0)

    UserInterfaceFlow.quick_run(UserInterfaceAlert("[ ] Database indexeren..."), 0)

    IndexService.index_database()

    UserInterfaceFlow.quick_run(UserInterfaceAlert("[+] Database geïndexeerd ", Color.OKGREEN), 0)

    DatabaseSeeder.seedScooters()

if __name__ == '__main__':
    main()
