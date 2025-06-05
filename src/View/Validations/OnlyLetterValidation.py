import re
from View.Validations.Validation import Validation


class OnlyLetterValidation(Validation):

    @staticmethod
    def validate(value: str) -> tuple[bool, str]:
        pattern = r'^[a-zA-Z\s]*$'
        if re.match(pattern, value):
            return True, ""

        return False, "Deze waarde mag alleen letters bevatten"