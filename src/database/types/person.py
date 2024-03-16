from __future__ import annotations

class Person:
    def __init__(self, id: int = 0, name: str = '', cathegory_ids: list = None, balance: int = 0) -> None:
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

    def __eq__(self, other_person: Person) -> bool:
        return (self.id == other_person.id
                and self.name == other_person.name
                and self.cathegory_ids == other_person.cathegory_ids
                and self.balance == other_person.balance)
