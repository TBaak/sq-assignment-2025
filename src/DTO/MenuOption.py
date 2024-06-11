class MenuOption:
    def __init__(self, name, action):
        self.name = name
        self.action = action

    def execute(self):
        self.action()