from View.Validations.Validation import Validation


class NotBlankValidation(Validation):

    @staticmethod
    def validate(value: str) -> tuple[bool, str]:
        if value != "":
            return True, ""
        return False, "Deze waarde mag niet leeg zijn"
