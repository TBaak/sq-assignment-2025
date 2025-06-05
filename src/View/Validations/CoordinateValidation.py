import re
from View.Validations.Validation import Validation


class CoordinateValidation(Validation):
    staticmethod
    def validate(value: str) -> tuple[bool, str]:
        coordinate_pattern = r'^-?\d{1,3}\.\d{5}\s-?\d{1,3}\.\d{5}$'

        if re.match(coordinate_pattern, value):

            # Valid coordinate format, now check if it's within Rotterdam
            lat, lon = CoordinateValidation.__split_lat_lng(value)

            if not CoordinateValidation.__is_within_rotterdam(lat, lon):
                return False, "De coördinaten moeten binnen Rotterdam liggen."

            return True, ""

        return False, "Dit veld moet een geldig coördinaat zijn in Rotterdam."

    @staticmethod
    def __is_within_rotterdam(lat, lon):
        return 51.85 <= lat <= 51.99 and 4.35 <= lon <= 4.55

    @staticmethod
    def __split_lat_lng(value):
        parts = value.split()
        lat = float(parts[0])
        lon = float(parts[1])
        return lat, lon