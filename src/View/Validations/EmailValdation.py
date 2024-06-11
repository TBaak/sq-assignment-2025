from View.Validations.Validation import Validation
import re

class EmailValidation(Validation):

    @staticmethod
    def validate(value: str) -> [bool, str]:
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not re.match(email_regex, value):
            return [False, value + " is geen geldig emailadres"]
        return [True, ""]
