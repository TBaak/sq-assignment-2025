from enum import Enum

from Security.Enum.Permission import Permission


class Role(Enum):
    SUPER_ADMIN = [
        Permission.MemberCreate.value,
        Permission.MemberRead.value,
        Permission.MemberUpdate.value,
        Permission.MemberDelete.value,

        Permission.UserConsultantCreate.value,
        Permission.UserConsultantRead.value,
        Permission.UserConsultantUpdate.value,
        Permission.UserConsultantDelete.value,
        Permission.UserConsultantResetPassword.value,

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
        Permission.MemberCreate.value,
        Permission.MemberRead.value,
        Permission.MemberUpdate.value,
        Permission.MemberDelete.value,

        Permission.UserConsultantCreate.value,
        Permission.UserConsultantRead.value,
        Permission.UserConsultantUpdate.value,
        Permission.UserConsultantDelete.value,
        Permission.UserConsultantResetPassword.value,

        Permission.UserUpdateOwnPassword.value,

        Permission.BackupCreate.value,
        Permission.BackupRestore.value,

        Permission.LogRead.value,
    ]
    CONSULTANT = [
        Permission.MemberCreate.value,
        Permission.MemberRead.value,
        Permission.MemberUpdate.value,

        Permission.UserUpdateOwnPassword.value,
    ]
