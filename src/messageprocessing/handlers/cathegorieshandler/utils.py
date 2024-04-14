

from database.api import DatabaseApi


def cathegories_to_string(income_cathegories, expense_cathegories) -> str:
    if len(income_cathegories) == 0 and len(expense_cathegories) == 0:
        return "Нам не удалось найти ни одной вашей категории."
    result = ""
    line_format = "{}. {}\n" "\tТекущие траты: {:,}\n" "\tЛимит: {:,}"
    start_number = 1
    for cathegory_type_name, cathegories in (
        ("Доходные категории", income_cathegories),
        ("Расходные категории", expense_cathegories),
    ):
        result += cathegory_type_name + ":\n"
        for seq_no, cathegory in enumerate(cathegories, start_number):
            line = line_format.format(
                seq_no, cathegory.name, cathegory.current_money, cathegory.money_limit
            )
            result += line + "\n"
            start_number = seq_no
        result += "\n\n"
    return result


def load_person_cathegories(person_id) -> tuple[list, list]:
    """
    Returns:
        (income_cathegories, expense_cathegories)
    
    Raise:
        Different database exceptions
    """
    cathegories = DatabaseApi().get_person_all_cathegories_by_id(person_id)
    income_cathegories = filter(
        lambda x: x.cathegory_type_id == DatabaseApi().get_income_cathegory_type_id(),
        cathegories,
    )
    income_cathegories = list(income_cathegories)
    expense_cathegories = filter(
        lambda x: x.cathegory_type_id == DatabaseApi().get_expense_cathegory_type_id(),
        cathegories,
    )
    expense_cathegories = list(expense_cathegories)
    return (income_cathegories, expense_cathegories)
