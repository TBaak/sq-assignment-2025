from tabulate import tabulate

from View.UserInterfaceFlowItem import UserInterfaceFlowItem
from View.UserInterfaceTableRow import UserInterfaceTableRow


class UserInterfaceTable(UserInterfaceFlowItem):
    rows: list[UserInterfaceTableRow] = []

    def __init__(self, rows: list[UserInterfaceTableRow]):
        self.rows = rows

    def render(self, is_retrying: bool = False):
        rows_formatted = list(map(lambda row: row.columns, self.rows))
        print(tabulate(rows_formatted, headers=['Optie', 'Menu actie'], tablefmt='fancy_grid'))
        return True, None
