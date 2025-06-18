from View.Validations.Validation import Validation


class AlphaNumericValidation(Validation):

    @staticmethod
    def validate(value: str) -> tuple[bool, str]:
        valueWithoutSpaces = value.replace(" ", "")

        if valueWithoutSpaces == "" or valueWithoutSpaces.isalnum():
            return True, ""

        return False, "Deze waarde moet uit getallen en/of letters bestaan"