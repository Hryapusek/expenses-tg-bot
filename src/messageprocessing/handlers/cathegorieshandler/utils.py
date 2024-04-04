def cathegories_to_string(income_cathegories, expense_cathegories) -> str:
        if len(income_cathegories) == 0 and len(expense_cathegories) == 0:
            return "Нам не удалось найти ни одной вашей категории."
        result = ""
        line_format = ("{}. {}\n"
                       "\tТекущие траты: {:,}\n"
                       "\tЛимит: {:,}")
        start_number = 1
        for cathegory_type_name, cathegories in (("Доходные категории", income_cathegories),
                                               ("Расходные категории", expense_cathegories)):
            result += cathegory_type_name + ":\n"
            for seq_no, cathegory in enumerate(cathegories, start_number):
                line = line_format.format(seq_no, cathegory.name, cathegory.current_money, cathegory.money_limit)
                result += line + '\n'
                start_number = seq_no
            result += '\n\n'
        return result