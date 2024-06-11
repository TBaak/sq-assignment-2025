from View.Validations.Validation import Validation


class OnlyNumberValidation(Validation):

    @staticmethod
    def validate(value: str) -> [bool, str]:
        if not value.isdigit():
            return [False, "Deze waarde mag alleen cijfers bevatten"]
        return [True, ""]