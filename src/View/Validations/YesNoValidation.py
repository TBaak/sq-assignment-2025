from View.Validations.Validation import Validation


class YesNoValidation(Validation):

    @staticmethod
    def validate(value: str) -> tuple[bool, str]:
        if value.lower() in ["y", "n"]:
            return True, ""

        return False, "Deze waarde moet y of n zijn"