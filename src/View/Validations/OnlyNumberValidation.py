from View.Validations.Validation import Validation


class OnlyNumberValidation(Validation):

    @staticmethod
    def validate(value: str) -> tuple[bool, str]:
        if value.isdigit():
            return True, ""

        return False, "Deze waarde mag alleen cijfers bevatten"
