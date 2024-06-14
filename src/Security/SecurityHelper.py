from Debug.ConsoleLogger import ConsoleLogger
from Models.User import User
from Security.Enum.Role import Role


class SecurityHelper(object):
    __loggedInUser: User = None

    @staticmethod
    def get_logged_in_user() -> User:
        return SecurityHelper.__loggedInUser

    @staticmethod
    def set_logged_in_user(user: User) -> bool:

        if not hasattr(Role, user.role):
            ConsoleLogger.v(f"UserHelper.set_logged_in_user: User role '{user.role}' not found")
            return False

        SecurityHelper.__loggedInUser = user
        return True
