import re

from View.Validations.Validation import Validation


class NoSpecialCharsValidation(Validation):

    @staticmethod
    def validate(value: str) -> [bool, str]:
        pattern = r'^[A-Za-z0-9 _]*[A-Za-z0-9][A-Za-z0-9 _]*$'
        if value is not "" and not re.match(pattern, value):
            return [False, "Deze waarde mag alleen letters bevatten"]
        return [True, ""]