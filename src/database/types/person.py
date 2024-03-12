
class Person:
    def __init__(self, id = 0, name = '', cathegory_ids = None, balance = 0) -> None:
        if not cathegory_ids:
            cathegory_ids = []
        self.id = id
        self.name = name
        self.cathegory_ids = cathegory_ids
        self.balance = balance

    @staticmethod
    def fromTuple(data):
        person = Person(
            id = data[0],
            name = data[1],
            cathegory_ids = data[2],
            balance = data[3]
            )
        return person
