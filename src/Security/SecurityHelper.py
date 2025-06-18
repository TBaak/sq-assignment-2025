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
            return False

        SecurityHelper.__loggedInUser = user
        return True
