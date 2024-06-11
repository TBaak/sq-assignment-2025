from View.Validations.Validation import Validation


class GenderValidation(Validation):

    @staticmethod
    def validate(value: str) -> [bool, str]:
        if value not in ["m", "v", "x"]:
            return [False, "Deze waarde moet m, v of x zijn"]
        return [True, ""]