import re
from View.Validations.Validation import Validation


class OnlyLetterValidation(Validation):

    @staticmethod
    def validate(value: str) -> [bool, str]:
        pattern = r'^[a-zA-Z\s]*$'
        if not re.match(pattern, value):
            return [False, "Deze waarde mag alleen letters bevatten"]
        return [True, ""]