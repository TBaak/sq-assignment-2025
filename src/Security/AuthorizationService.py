from Enum.Color import Color
from Security.Enum.Permission import Permission
from Security.Enum.Role import Role
from Security.SecurityHelper import SecurityHelper
from View.UserInterfaceAlert import UserInterfaceAlert
from View.UserInterfaceFlow import UserInterfaceFlow


class AuthorizationService:

    @staticmethod
    def current_user_has_permission(permission: Permission) -> bool:
        user = SecurityHelper.get_logged_in_user()

        if user is None:
            return False

        if permission.value in Role[user.role].value:
            return True

        return False

    @staticmethod
    def show_not_allowed_alert() -> object:
        UserInterfaceFlow.quick_run(
            UserInterfaceAlert("U heeft geen rechten om deze actie uit te voeren", Color.FAIL),
            2
        )
        return
