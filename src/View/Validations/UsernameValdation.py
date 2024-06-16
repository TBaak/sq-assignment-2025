from Service.IndexService import IndexService
from View.Validations.Validation import Validation
import re


class UsernameValidation(Validation):

    @staticmethod
    def validate(value: str) -> [bool, str]:
        pattern = r"(?i)^[a-z_][a-z0-9_'.]{7,9}$"

        if value is not "" and not re.match(pattern, value):
            return [False, "Username moet tussen 8 en 10 karakters lang zijn, beginnen met een letter of "
                           "underscore (_), en alleen letters, cijfers, underscores (_), apostrofes ('), "
                           "en punten (.) bevatten."]

        existingUser = IndexService.find_user_by_username(value)

        if existingUser is not None:
            return [False, "Deze username is al in gebruik"]

        return [True, ""]
