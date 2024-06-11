class UserInterfaceTableRow:
    columns: list[str] = []

    def __init__(self, columns=None):
        if columns is None:
            columns = []
        self.columns = columns

    def addColumn(self, text: str):
        self.columns.append(text)