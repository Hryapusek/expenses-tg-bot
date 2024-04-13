from telebot.types import ReplyKeyboardMarkup

class GetMoneyLimitConstrains:
    ASKING_MESSAGE = "Введите желаемое ограничение по сумме для данной категории"
    BAD_LIMIT_MESSAGE = "Введено некорректное значение. Попробуйте снова"

    MARKUP = ReplyKeyboardMarkup()
    MARKUP.add("0", "1000")
    MARKUP.add("5000", "10000")
    MARKUP.add("20000", "30000")

    @staticmethod
    def is_valid_money_limit(limit: str) -> tuple[bool, str]:
        if limit <= 0:
            return (False, __class__.BAD_LIMIT_MESSAGE)
        return (True, "")
        
class GetNameConstrains:
    ASKING_MESSAGE = "Введите название категории"
    ERROR_MESSAGE = "Имя не может быть пустым"

    @staticmethod
    def is_valid_name(name: str) -> tuple[bool, str]:
        if len(name) == 0:
            return (False, __class__.ERROR_MESSAGE)
        return (True, "")
    
class GetCurrentMoneyConstrains:
    ASKING_MESSAGE = "Введите текущие затраты/доходы по данной категории"
    BAD_LIMIT_MESSAGE = "Введено некорректное значение. Попробуйте снова"

    MARKUP = ReplyKeyboardMarkup()
    MARKUP.add("0", "1000")
    MARKUP.add("5000", "10000")
    MARKUP.add("20000", "30000")