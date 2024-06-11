from View.Validations.Validation import Validation


class NotBlankValidation(Validation):

    @staticmethod
    def validate(value: str) -> [bool, str]:
        if value == "":
            return [False, "Deze waarde mag niet leeg zijn"]
        return [True, ""]