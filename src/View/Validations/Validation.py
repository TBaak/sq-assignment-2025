class Validation(object):

    @staticmethod
    def validate(value: str) -> tuple[bool, str]:
        raise NotImplementedError("This method should be implemented by the subclass")
