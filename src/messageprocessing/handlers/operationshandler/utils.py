from database.api import DatabaseApi
from database.types.operation import Operation


def operation_to_str(operation: Operation) -> str:
    """
    Raise
    -----
        - Different database exceptions
    """
    cathegory_name = DatabaseApi().get_cathegory_by_id(operation.cathegory_id).name
    operation_str = (f"Категория: {cathegory_name}\n"
                     f"\tИзменение баланса: {operation.money_amount}\n"
                     f"\tКомментарий: {operation.comment[:50] + '...' if len(operation.comment) > 50 else operation.comment}")
    return operation_str
