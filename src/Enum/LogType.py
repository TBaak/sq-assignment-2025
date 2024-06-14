from enum import Enum

from DTO.LogType import LogTypeDTO


class LogType(Enum):
    UserSystemAdminCreated = LogTypeDTO("User admin is created")
    UserSystemAdminRead = LogTypeDTO("User admin is read")
    UserSystemAdminsRead = LogTypeDTO("Users admin are read")
    UserSystemAdminUpdated = LogTypeDTO("User admin is updated")
    UserSystemAdminDeleted = LogTypeDTO("User admin is deleted")

    UserConsultantCreated = LogTypeDTO("User consultant is created")
    UserConsultantRead = LogTypeDTO("User consultant is read")
    UserConsultantsRead = LogTypeDTO("Users consultant are read")
    UserConsultantUpdated = LogTypeDTO("User consultant is updated")
    UserConsultantDeleted = LogTypeDTO("User consultant is deleted")

    MemberCreated = LogTypeDTO("Member is created")
    MemberRead = LogTypeDTO("Member is read")
    MembersRead = LogTypeDTO("Member is read")
    MemberUpdated = LogTypeDTO("Member is updated")
    MemberDeleted = LogTypeDTO("Member is deleted")

    BackupCreated = LogTypeDTO("Backup is created")
    BackupRestored = LogTypeDTO("Backup is restored")

    SuccessfulLogin = LogTypeDTO("Logged in")
    UnsuccessfulLogin = LogTypeDTO("Unsuccessful login")
    UnsuccessfulLoginSuspicious = LogTypeDTO("Unsuccessful login", True)

    PasswordReset = LogTypeDTO("PasswordReset")
    OwnPasswordUpdated = LogTypeDTO("OwnPasswordUpdated")


