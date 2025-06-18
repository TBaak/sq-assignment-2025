from View.Validations.Validation import Validation


class GenderValidation(Validation):

    @staticmethod
    def validate(value: str) -> tuple[bool, str]:
        if value.lower() in ["m", "v", "x"]:
            return True, ""

        return False, "Deze waarde moet m, v of x zijn"