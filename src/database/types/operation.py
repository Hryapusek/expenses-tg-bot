from __future__ import annotations
import datetime

class Operation:
    def __init__(
        self,
        id=0,
        date=datetime.datetime.now(),
        operation_type_id=0,
        person_id=0,
        cathegory_id=0,
        money_amount=0,
        comment="",
    ):
        self.id = id
        self.date = date
        self.operation_type_id = operation_type_id
        self.person_id = person_id
        self.cathegory_id = cathegory_id
        self.money_amount = money_amount
        self.comment = comment

    @staticmethod
    def fromTuple(data):
        operation = Operation(
            id=data[0],
            date=data[1],
            operation_type_id=data[2],
            person_id=data[3],
            cathegory_id=data[4],
            money_amount=data[5],
            comment=data[6],
        )
        return operation

    def __eq__(self, other: Operation) -> bool:
        return (
            self.id == other.id
            and self.date == other.date
            and self.operation_type_id == other.operation_type_id
            and self.cathegory_id == other.cathegory_id
            and self.money_amount == other.money_amount
            and self.comment == other.comment
        )
