from View.Validations.Validation import Validation


class AlphaNumericValidation(Validation):

    @staticmethod
    def validate(value: str) -> tuple[bool, str]:
        if value.isalnum():
            return True, ""

        return False, "Deze waarde moet een getal zijn"