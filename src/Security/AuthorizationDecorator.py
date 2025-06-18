from Security.AuthorizationService import AuthorizationService
from Security.Enum.Permission import Permission


class Auth:

    @staticmethod
    def permission_required(permission: Permission):
        def decorator(func):
            def wrapper(*args, **kwargs):
                if not AuthorizationService.current_user_has_permission(permission):
                    AuthorizationService.show_not_allowed_alert()
                    return
                return func(*args, **kwargs)

            return wrapper

        return decorator