from Service.EncryptionService import EncryptionService


class SerializeableModel:

    def serialize(self) -> dict:
        # Build a dict from fields and values
        serialized = {}
        for key in self.__dict__:
            if key.startswith("_"):
                continue
            value = self.__dict__[key]
            if isinstance(value, SerializeableModel):
                serialized[key] = value.serialize()
            elif isinstance(value, list):
                serialized[key] = []
                for item in value:
                    if isinstance(item, SerializeableModel):
                        serialized[key].append(item.serialize())
                    else:
                        serialized[key].append(item)
            else:
                serialized[key] = value

        return serialized
