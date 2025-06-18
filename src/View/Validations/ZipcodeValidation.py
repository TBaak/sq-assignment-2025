import re
from View.Validations.Validation import Validation


class ZipcodeValidation(Validation):

    @staticmethod
    def validate(value: str) -> tuple[bool, str]:
        dutch_zipcode_pattern = r'^[1-9][0-9]{3}[A-Z]{2}$'

        if re.match(dutch_zipcode_pattern, value):
            return True, ""

        return False, "Dit veld moet een geldige postcode zijn."
