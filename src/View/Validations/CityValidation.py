from View.Validations.Validation import Validation
import re


class CityValidation(Validation):

    @staticmethod
    def validate(value: str) -> tuple[bool, str]:
        allowed_cities = [
            "Den Haag",
            "Rotterdam",
            "Amsterdam",
            "Utrecht",
            "Eindhoven",
            "Tilburg",
            "Groningen",
            "Almere",
            "Breda",
            "Nijmegen",
        ]

        if value in allowed_cities:
            return True, ""

        return False, "Selecteer een stad. Kies uit: Den Haag, Rotterdam, Amsterdam, Utrecht, Eindhoven, Tilburg, Groningen, Almere, Breda, Nijmegen"
