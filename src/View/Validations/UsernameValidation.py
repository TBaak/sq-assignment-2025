from Service.IndexService import IndexService
from View.Validations.Validation import Validation
import re


class UsernameValidation(Validation):

    @staticmethod
    def validate(value: str) -> tuple[bool, str]:
        pattern = r"(?i)^[a-z_][a-z0-9_'.]{7,9}$"

        if re.match(pattern, value):

            # Valid but has to be unique
            existing_user = IndexService.find_user_by_username(value)
            if existing_user is not None:
                return False, "Deze username is al in gebruik"

            return True, ""




        return False, "Username moet tussen 8 en 10 karakters lang zijn, beginnen met een letter of underscore (_), en alleen letters, cijfers, underscores (_), apostrofes ('), en punten (.) bevatten."
