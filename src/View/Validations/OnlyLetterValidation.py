import re
from View.Validations.Validation import Validation


class OnlyLetterValidation(Validation):

    @staticmethod
    def validate(value: str) -> tuple[bool, str]:

        if value.isalpha():
            return True, ""

        return False, "Deze waarde mag alleen letters bevatten"