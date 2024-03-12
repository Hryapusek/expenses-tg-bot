class OperationType:
    def __init__(self, id = 0, type = ''):
        self.id = id
        self.type = type

    @staticmethod
    def fromTuple(data):
        operation_type_obj = OperationType (
            id = data[0],
            type = data[1]
        )
        return operation_type_obj