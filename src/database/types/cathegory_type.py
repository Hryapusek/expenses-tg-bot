class CathegoryType:
    def __init__(self, id = 0, type = ''):
        self.id = id
        self.type = type

    @staticmethod
    def fromTuple(data):
        cathegory_type_obj = CathegoryType (
            id = data[0],
            type = data[1]
        )
        return cathegory_type_obj