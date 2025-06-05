from View.Validations.Validation import Validation


class NumberMaxValidation(Validation):

    def __init__(self, max_value: int):
        self.max_value = max_value

    def validate(self, value: str) -> tuple[bool, str]:
        if value.isdigit() and int(value) <= self.max_value:
            return True, ""

        return False, f"Deze waarde mag niet meer dan {self.max_value} zijn"