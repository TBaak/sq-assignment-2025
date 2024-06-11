from Models.User import User


class UserHelper(object):
    __loggedInUser: User = None

    @staticmethod
    def get_logged_in_user() -> User:
        return UserHelper.__loggedInUser

    @staticmethod
    def set_logged_in_user(user: User) -> None:
        UserHelper.loggedInUser = user

    @staticmethod
    def has_permission(role) -> bool:
        # TODO: Implement this
        return True
