from View.Validations.Validation import Validation
import re


class EmailValidation(Validation):

    @staticmethod
    def validate(value: str) -> tuple[bool, str]:
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if re.match(email_regex, value):
            return True, ""

        return False, "Dit veld moet een email adres zijn"
