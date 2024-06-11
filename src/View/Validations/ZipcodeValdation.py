import re
from View.Validations.Validation import Validation


class ZipcodeValidation(Validation):

    @staticmethod
    def validate(value: str) -> [bool, str]:
        dutch_zipcode_pattern = r'^[1-9][0-9]{3}[A-Z]{2}$'

        if not re.match(dutch_zipcode_pattern, value):
            return [False, value + " is geen geldige postcode"]
        return [True, ""]
