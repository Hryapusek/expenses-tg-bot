from __future__ import annotations

class Cathegory:
    def __init__(self, id: int, person_id: int, cathegory_type_id: int, 
                 name: str, money_limit: int, current_money: int) -> None:
        self.id = id
        self.person_id = person_id
        self.cathegory_type_id = cathegory_type_id
        self.name = name
        self.money_limit = money_limit
        self.current_money = current_money

    @staticmethod
    def fromTuple(data):
        cathegory = Cathegory (
            id = data[0],
            person_id = data[1],
            cathegory_type_id = data[2],
            name = data[3],
            money_limit = data[4],
            current_money = data[5],
        )
        return cathegory
    
    def __eq__(self, other: Cathegory) -> bool:
        return (self.id == other.id and
                self.person_id == other.person_id and
                self.cathegory_type_id == other.cathegory_type_id and
                self.name == other.name and
                self.money_limit == other.money_limit and
                self.current_money == other.current_money)
