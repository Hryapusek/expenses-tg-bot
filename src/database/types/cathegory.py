class Cathegory:
    def __init__(self, id, person_id, cathegory_type_id, name, money_limit, current_money) -> None:
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
