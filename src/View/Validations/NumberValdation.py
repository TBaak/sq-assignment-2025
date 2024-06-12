from View.Validations.Validation import Validation


class NumberValidation(Validation):

    @staticmethod
    def validate(value: str) -> [bool, str]:
        if value is not "" and not value.isdigit():
            return [False, "Deze waarde moet een getal zijn"]
        return [True, ""]