import re
from View.Validations.Validation import Validation


class DateValidation(Validation):

    @staticmethod
    def validate(value: str) -> tuple[bool, str]:
        date_pattern = r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$'

        if re.match(date_pattern, value):
            return True, ""

        return False, "Ongeldige datum, gebruik YYYY-MM-DD"
