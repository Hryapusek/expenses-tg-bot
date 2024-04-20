from database.types.cathegory import Cathegory
from messageprocessing.botstate.bot_state import BotState
from messageprocessing.handlers.base_handler import ReusableHandler
from messageprocessing.handlers.commonhandlers.get_number_handler import GetNumberHandler
from ..base_inner_handler import ReturningResultHandler
from telebot.types import Message, ReplyKeyboardMarkup
from .utils import cathegories_to_string


class ChooseCathegoryHandler(ReturningResultHandler, ReusableHandler):
    """
        It is important to note, that when printing cathegories to choose from -
        INCOME cathegories always go first.
    """
    CHOOSE_CATHEGORY_MESSAGE = "\n\nВведите номер категории"
    BAD_NUMBER_MESSAGE = "Введите корректный номер категории"

    def __init__(
        self,
        outter_handler: ReusableHandler,
        income_cathegories: list[Cathegory],
        expense_cathegories: list[Cathegory],
        markup,
    ) -> None:
        super().__init__(outter_handler)
        self.income_cathegories = income_cathegories
        self.expense_cathegories = expense_cathegories
        self.markup = markup

    def handle_message(self, message: Message):
        assert False, "This should not be called. Silly mistake maybe made???"
        return self

    def switch_to_existing_handler(self, message: Message) -> ReusableHandler:
        if self.return_result == None:
            self.outter_handler.return_result = None
            return self.outter_handler.switch_to_existing_handler(message)
        cathegory_number = self.return_result
        index = cathegory_number - 1 # Enumerations begins with one
        if index >= len(self.income_cathegories):
            index -= len(self.income_cathegories)
            cathegory = self.expense_cathegories[index]
            self.outter_handler.return_result = (cathegory, self.expense_cathegories, index)
        else:
            cathegory = self.income_cathegories[index]
            self.outter_handler.return_result = (cathegory, self.income_cathegories, index)
        return self.outter_handler.switch_to_existing_handler(message)

    @staticmethod
    def switch_to_this_handler(
        message: Message,
        outter_handler,
        income_cathegories: list[Cathegory],
        expense_cathegories: list[Cathegory],
    ):
        """
        return_result:
            - None if canceled or empty
            - (Cathegory, List, Index) otherwise
        """
        markup = ReplyKeyboardMarkup()
        n_cathegories = len(income_cathegories) + len(expense_cathegories)
        if n_cathegories == 0:
            outter_handler.return_result = None
            BotState().bot.send_message(message.from_user.id, "Не найдена ни одна категория")
            return outter_handler.switch_to_existing_handler(message)
        for buttons in _generate_triples(n_cathegories):
            markup.add(*(btn for btn in buttons if btn != None))
        handler = __class__(
            outter_handler, income_cathegories, expense_cathegories, markup
        )
        def pred(num):
            if num < 1 or num > n_cathegories:
                return (False, "Номер категории не вошел в указанный диапозон. Попробуйте снова.")
            return (True, "")
        asking_message = ""
        asking_message += cathegories_to_string(income_cathegories, expense_cathegories) + __class__.CHOOSE_CATHEGORY_MESSAGE
        return GetNumberHandler.switch_to_this_handler(message, handler, asking_message, markup, pred)


def _generate_triples(last_number: int):
    for i in range(1, (last_number) // 3 + 1):
        yield (str(i), str(i + 1), str(i + 2))

    if last_number % 3 == 1:
        yield (str(last_number), None, None)
    elif last_number % 3 == 2:
        yield (str(last_number - 1), str(last_number), None)
