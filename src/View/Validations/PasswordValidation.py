from Service.IndexService import IndexService
from View.Validations.Validation import Validation
import re


class PasswordValidation(Validation):

    @staticmethod
    def validate(value: str) -> tuple[bool, str]:
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_\-+=`|\\(){}[\]:;'<>,.?/])[A-Za-z\d~!@#$%&_\-+=`|\\(){}[\]:;'<>,.?/]{12,30}$"

        if re.match(pattern, value):
            return True, ""

        return False, "Het wachtwoord moet tussen 12 en 30 karakters lang zijn, mag letters (a-z, A-Z), cijfers (0-9), en speciale tekens (~!@#$%&_-+=`|\\(){}[]:;'<>,.?/) bevatten, en moet minimaal één kleine letter, één hoofdletter, één cijfer, en één speciaal teken bevatten."
