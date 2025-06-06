import re

from View.Validations.Validation import Validation


class NoSpecialCharsValidation(Validation):

    @staticmethod
    def validate(value: str) -> tuple[bool, str]:
        pattern = r'^[A-Za-z0-9 _]*[A-Za-z0-9][A-Za-z0-9 _]*$'
        if re.match(pattern, value):
            return True, ""

        return False, "Deze waarde mag alleen letters bevatten"