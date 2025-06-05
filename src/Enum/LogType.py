from enum import Enum

from DTO.LogType import LogTypeDTO


class LogType(Enum):
    UserSystemAdminCreated = LogTypeDTO("User admin is created")
    UserSystemAdminRead = LogTypeDTO("User admin is read")
    UserSystemAdminsRead = LogTypeDTO("Users admin are read")
    UserSystemAdminUpdated = LogTypeDTO("User admin is updated")
    UserSystemAdminDeleted = LogTypeDTO("User admin is deleted")

    UserServiceEngineerCreated = LogTypeDTO("User service engineer is created")
    UserServiceEngineerRead = LogTypeDTO("User service engineer is read")
    UserServiceEngineersRead = LogTypeDTO("Users service engineer are read")
    UserServiceEngineerUpdated = LogTypeDTO("User service engineer is updated")
    UserServiceEngineerDeleted = LogTypeDTO("User service engineer is deleted")

    TravellerCreated = LogTypeDTO("Traveller is created")
    TravellerRead = LogTypeDTO("Traveller is read")
    TravellersRead = LogTypeDTO("Traveller is read")
    TravellerUpdated = LogTypeDTO("Traveller is updated")
    TravellerDeleted = LogTypeDTO("Traveller is deleted")

    BackupCreated = LogTypeDTO("Backup is created")
    BackupRestored = LogTypeDTO("Backup is restored")

    SuccessfulLogin = LogTypeDTO("Logged in")
    UnsuccessfulLogin = LogTypeDTO("Unsuccessful login")
    UnsuccessfulLoginSuspicious = LogTypeDTO("Unsuccessful login", True)

    NullByteInput = LogTypeDTO("Null byte input", True)

    PasswordReset = LogTypeDTO("Password reset")
    OwnPasswordUpdated = LogTypeDTO("Own password is updated")


