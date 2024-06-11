from View.Validations.Validation import Validation


class NumberValidation(Validation):

    @staticmethod
    def validate(value: str) -> [bool, str]:
        if not value.isdigit():
            return [False, "Deze waarde moet een getal zijn"]
        return [True, ""]