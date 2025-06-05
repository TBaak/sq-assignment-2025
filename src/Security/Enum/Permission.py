from enum import Enum


class Permission(Enum):
    TravellerCreate = "traveller_create"
    TravellerRead = "traveller_read"
    TravellerUpdate = "traveller_update"
    TravellerDelete = "traveller_delete"

    ScooterUpdateFull = "scooter_update_full"
    ScooterUpdatePartial = "scooter_update_partial"

    UserServiceEngineerCreate = "user_service_engineer_create"
    UserServiceEngineerRead = "user_service_engineer_read"
    UserServiceEngineerUpdate = "user_service_engineer_update"
    UserServiceEngineerDelete = "user_service_engineer_delete"
    UserServiceEngineerResetPassword = "user_service_engineer_reset_password"

    UserSystemAdminCreate = "user_system_admin_create"
    UserSystemAdminRead = "user_system_admin_read"
    UserSystemAdminUpdate = "user_system_admin_update"
    UserSystemAdminDelete = "user_system_admin_delete"
    UserSystemAdminResetPassword = "user_system_admin_reset_password"

    UserUpdateOwnPassword = "user_update_own_password"

    BackupCreate = "backup_create"
    BackupRestore = "backup_restore"

    LogRead = "log_read"
