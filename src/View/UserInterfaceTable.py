from tabulate import tabulate

from View.UserInterfaceFlowItem import UserInterfaceFlowItem
from View.UserInterfaceTableRow import UserInterfaceTableRow


class UserInterfaceTable(UserInterfaceFlowItem):
    rows: list[UserInterfaceTableRow] = []
    has_header: bool = False

    def __init__(self, rows: list[UserInterfaceTableRow], has_header: bool = False):
        self.rows = rows
        self.has_header = has_header

    def render(self, is_retrying: bool = False):
        rows_formatted = list(map(lambda row: row.columns, self.rows))
        if self.has_header:
            print(tabulate(rows_formatted, headers="firstrow"))
        else:
            print(tabulate(rows_formatted))
        return True, None

    @staticmethod
    def add_row_numbers(rows: list[list[str]]):
        for index, row in enumerate(rows):
            row.insert(0, str(index + 1))
        return rows
