from View.Validations.Validation import Validation


class LengthValidation(Validation):

    def __init__(self, length: int):
        self.length = length

    def validate(self, value: str) -> [bool, str]:
        if len(value) != self.length:
            return [False, f"Deze waarde moet {self.length} tekens lang zijn"]
        return [True, ""]