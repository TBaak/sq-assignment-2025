import re
from View.Validations.Validation import Validation


class DriverLicenseValidation(Validation):

    @staticmethod
    def validate(value: str) -> tuple[bool, str]:
        dl_pattern = r'^(?:[A-Z]{2}[0-9]{7}|[A-Z][0-9]{8})$'

        if re.match(dl_pattern, value):
            return True, ""

        return False, "Dit veld moet een geldig rijbewijs nummer zijn. (bijv. XXDDDDDDD of XDDDDDDDD, waarbij X een letter is en D een cijfer)"
