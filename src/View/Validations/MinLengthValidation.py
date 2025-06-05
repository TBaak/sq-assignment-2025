from View.Validations.Validation import Validation


class MinLengthValidation(Validation):

    def __init__(self, length: int):
        self.length = length

    def validate(self, value: str) -> tuple[bool, str]:
        if len(value) >= self.length:
            return True, ""

        return False, f"Deze waarde mag niet minder dan {self.length} tekens lang zijn"