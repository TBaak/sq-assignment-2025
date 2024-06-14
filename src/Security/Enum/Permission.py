from enum import Enum


class Permission(Enum):
    MemberCreate = "member_create"
    MemberRead = "member_read"
    MemberUpdate = "member_update"
    MemberDelete = "member_delete"

    UserConsultantCreate = "user_consultant_create"
    UserConsultantRead = "user_consultant_read"
    UserConsultantUpdate = "user_consultant_update"
    UserConsultantDelete = "user_consultant_delete"
    UserConsultantResetPassword = "user_consultant_reset_password"

    UserSystemAdminCreate = "user_system_admin_create"
    UserSystemAdminRead = "user_system_admin_read"
    UserSystemAdminUpdate = "user_system_admin_update"
    UserSystemAdminDelete = "user_system_admin_delete"
    UserSystemAdminResetPassword = "user_system_admin_reset_password"

    UserUpdateOwnPassword = "user_update_own_password"

    BackupCreate = "backup_create"
    BackupRestore = "backup_restore"

    LogRead = "log_read"
