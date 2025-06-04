from enum import Enum

from Security.Enum.Permission import Permission


class Role(Enum):
    SUPER_ADMIN = [
        Permission.TravellerCreate.value,
        Permission.TravellerRead.value,
        Permission.TravellerUpdate.value,
        Permission.TravellerDelete.value,

        Permission.UserServiceEngineerCreate.value,
        Permission.UserServiceEngineerRead.value,
        Permission.UserServiceEngineerUpdate.value,
        Permission.UserServiceEngineerDelete.value,
        Permission.UserServiceEngineerResetPassword.value,

        Permission.UserSystemAdminCreate.value,
        Permission.UserSystemAdminRead.value,
        Permission.UserSystemAdminUpdate.value,
        Permission.UserSystemAdminDelete.value,
        Permission.UserSystemAdminResetPassword.value,

        # Permission.UserUpdateOwnPassword.value, Not possible because it is hardcodes

        Permission.BackupCreate.value,
        Permission.BackupRestore.value,

        Permission.LogRead.value,
    ]
    SYSTEM_ADMIN = [
        Permission.TravellerCreate.value,
        Permission.TravellerRead.value,
        Permission.TravellerUpdate.value,
        Permission.TravellerDelete.value,

        Permission.UserServiceEngineerCreate.value,
        Permission.UserServiceEngineerRead.value,
        Permission.UserServiceEngineerUpdate.value,
        Permission.UserServiceEngineerDelete.value,
        Permission.UserServiceEngineerResetPassword.value,

        Permission.UserUpdateOwnPassword.value,

        Permission.BackupCreate.value,
        Permission.BackupRestore.value,

        Permission.LogRead.value,
    ]
    SERVICE_ENGINEER = [
        Permission.UserUpdateOwnPassword.value,
    ]
