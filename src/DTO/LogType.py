class LogTypeDTO:
    message: str
    suspicious: bool

    def __init__(self, message: str, suspicious: bool = False):
        self.message = message
        self.suspicious = suspicious
