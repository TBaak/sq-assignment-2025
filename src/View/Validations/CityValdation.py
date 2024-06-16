from View.Validations.Validation import Validation
import re

class CityValidation(Validation):

    @staticmethod
    def validate(value: str) -> [bool, str]:

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


        if value is not "" and value not in allowed_cities:
            return [False, value + " is geen geldige stad. "
                                   "Kies uit: Den Haag, Rotterdam, Amsterdam, Utrecht, Eindhoven, Tilburg, Groningen, "
                                   "Almere, Breda, Nijmegen"]
        return [True, ""]
