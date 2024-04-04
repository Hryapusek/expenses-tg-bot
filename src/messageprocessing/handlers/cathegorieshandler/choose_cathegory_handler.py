from database.types.cathegory import Cathegory
from messageprocessing.botstate.bot_state import BotState
from messageprocessing.handlers.base_hndl import ReusableHandler
from ..base_inner_hndl import ReturningResultHandler
from telebot.types import Message, ReplyKeyboardMarkup
from .utils import cathegories_to_string


class ChooseCathegoryHandler(ReturningResultHandler):
    CHOOSE_CATHEGORY_MESSAGE = "\n\nВведите номер категории"
    BAD_NUMBER_MESSAGE = "Введите корректный номер категории"
    CANCEL_BUTTON = "Отменить"

    def __init__(self, outter_handler: ReusableHandler, income_cathegories: list[Cathegory],
                 expense_cathegories: list[Cathegory], markup) -> None:
        super().__init__(outter_handler)
        self.income_cathegories = income_cathegories
        self.expense_cathegories = expense_cathegories
        self.markup = markup

    def handle_message(self, message: Message):
        if not message.text:
            BotState().bot.send_message(__class__.CHOOSE_CATHEGORY_MESSAGE, reply_markup=self.markup)    
            return self
        if message.text == __class__.CANCEL_BUTTON:
            self.outter_handler.return_result = None
            return self.outter_handler.switch_to_existing_handler(message)
        try:
            n_cathegories = len(self.income_cathegories) + len(self.expense_cathegories)
            number = int(message.text)
            if number > n_cathegories or number < 1:
                BotState().bot.send_message(__class__.BAD_NUMBER_MESSAGE, reply_markup=self.markup)    
                return self
            self.outter_handler.return_result = number
            return self.outter_handler.switch_to_existing_handler(message)
        except ValueError:
            BotState().bot.send_message(__class__.BAD_NUMBER_MESSAGE, reply_markup=self.markup)    
            return self

    @staticmethod
    def switch_to_this_handler(message: Message, outter_handler, income_cathegories: list[Cathegory],
                                expense_cathegories: list[Cathegory]):
        """
        Notes:
            Check cathegories for empiness before calling!
        """
        markup = ReplyKeyboardMarkup()
        n_cathegories = len(income_cathegories) + len(expense_cathegories)
        for buttons in _generate_triples(n_cathegories):
            markup.add(*(btn for btn in buttons if btn != None))
        markup.add(__class__.CANCEL_BUTTON, row_width=3)
        handler = __class__(outter_handler, income_cathegories, expense_cathegories, markup)
        result = ""
        result += cathegories_to_string(income_cathegories, expense_cathegories)
        BotState().bot.send_message(message.chat.id, result + __class__.CHOOSE_CATHEGORY_MESSAGE, reply_markup=markup)
        return handler

def _generate_triples(last_number: int):
    for i in range(1, (last_number)//3 + 1):
        yield (str(i), str(i+1), str(i+2))
    
    if last_number % 3 == 1:
        yield (str(last_number), None, None)
    elif last_number % 3 == 2:
        yield (str(last_number-1), str(last_number), None)
