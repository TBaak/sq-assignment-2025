from View.Validations.Validation import Validation


class NumberMinValidation(Validation):

    def __init__(self, min_value: int):
        self.min_value = min_value

    def validate(self, value: str) -> tuple[bool, str]:
        if value.isdigit() and int(value) <= self.min_value:
            return True, ""

        return False, f"Deze waarde mag niet minder dan {self.min_value} zijn"