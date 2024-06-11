class DatabaseModel:

    def populate(self, data, fields):
        for index, field in enumerate(fields):
            setattr(self, field, data[index])
