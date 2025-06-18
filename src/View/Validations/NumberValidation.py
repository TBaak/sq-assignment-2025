from View.Validations.Validation import Validation


class NumberValidation(Validation):

    @staticmethod
    def validate(value: str) -> tuple[bool, str]:
        if value.isdigit():
            return True, ""

        return False, "Deze waarde moet een getal zijn"