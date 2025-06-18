import re
from warnings import deprecated

from View.Validations.Validation import Validation


@deprecated("NoSpecialCharsValidation is deprecated, use OnlyLetterValidation instead.")
class NoSpecialCharsValidation(Validation):

    @staticmethod
    def validate(value: str) -> tuple[bool, str]:
        valueWithoutSpaces = value.replace(" ", "")

        if valueWithoutSpaces == "" or valueWithoutSpaces.isalnum():
            return True, ""

        return False, "Deze waarde mag alleen letters bevatten"