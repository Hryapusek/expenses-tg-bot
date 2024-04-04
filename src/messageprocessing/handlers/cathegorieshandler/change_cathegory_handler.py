from __future__ import annotations
from database.api import DatabaseApi
from database.types.cathegory import Cathegory
from messageprocessing.botstate.bot_state import BotState
from messageprocessing.handlers.base_hndl import BaseHandler
from messageprocessing.handlers.base_inner_hndl import BaseInnerHandler
from ..base_hndl import ReusableHandler
from telebot.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from .utils import cathegories_to_string
from .choose_cathegory_handler import ChooseCathegoryHandler


class ChangeCathegoryHandler(ReusableHandler, BaseInnerHandler):

    CHOOSE_OPTION_MESSAGE = "\n\nВыберите что хотите изменить"
    MARKUP = ReplyKeyboardMarkup()
    NAME_BUTTON = "Название"
    TYPE_BUTTON = "Тип"
    CURRENT_MONEY_BUTTON = "Текущие траты"
    LIMIT_BUTTON = "Лимит"
    BACK_BUTTON = "Назад"
    MARKUP.add(NAME_BUTTON)
    MARKUP.add(TYPE_BUTTON)
    MARKUP.add(CURRENT_MONEY_BUTTON)
    MARKUP.add(LIMIT_BUTTON)
    MARKUP.add(BACK_BUTTON)

    WAITING_FOR_CATHEGORY = 1
    WAITING_FOR_NAME = 2
    WAITING_FOR_TYPE = 3
    WAITING_FOR_CURRENT_MONEY = 4
    WAITING_FOR_LIMIT = 5

    def __init__(self, outter_handler: BaseHandler) -> None:
        super().__init__(outter_handler)
        self.state = __class__.WAITING_FOR_CATHEGORY

    def handle_message(self, message: Message):
        if not message.text:
            return self
        
        return self
        

    @staticmethod
    def switch_to_this_handler(message: Message, outter_handler):
        this_handler = __class__(outter_handler)
        return ChooseCathegoryHandler.switch_to_this_handler(message, this_handler,
                                                             outter_handler.income_cathegories,
                                                             outter_handler.expense_cathegories)

    def switch_to_existing_handler(self, message: Message):
        if self.state == __class__.WAITING_FOR_CATHEGORY:
            return self.got_cathegory(message)
        elif self.state == __class__.WAITING_FOR_NAME:
            return self.got_name(message)

    def got_cathegory(self, message: Message) -> ChangeCathegoryHandler:
        if not self.return_result:
            return self.outter_handler.switch_to_existing_handler(message)
        self.cathegory_num = self.return_result
        del self.return_result
        if self.cathegory_num <= len(self.outter_handler.income_cathegories):
            self.cathegory_list = self.outter_handler.income_cathegories
            self.cathegory_num -= 1
        else:
            self.cathegory_list = self.outter_handler.expense_cathegories
            self.cathegory_num -= len(self.outter_handler.income_cathegories) + 1
        self.cathegory: Cathegory = self.cathegory_list[self.cathegory_num]
        self.show_cathegory(message)
        return self

    def show_cathegory(self, message: Message):
        line_format = ("Название: {}\n"
                       "Тип: {}\n"
                       "Текущие траты: {:,}\n"
                       "Лимит: {:,}")
        result_str = line_format.format(self.cathegory.name,
                                        "Расходы" if self.cathegory.cathegory_type_id == DatabaseApi().get_expense_cathegory_type_id()
                                        else "Доходы",
                                        self.cathegory.current_money,
                                        self.cathegory.money_limit) + __class__.CHOOSE_OPTION_MESSAGE
        BotState().bot.send_message(message.chat.id, result_str, reply_markup=__class__.MARKUP)

    def got_name(self, message: Message):
        
        pass


def _generate_triples(last_number: int):
    for i in range(1, (last_number)/3 + 1):
        yield (str(i), str(i+1), str(i+2))
    
    if last_number % 3 == 1:
        return (str(last_number), None, None)
    elif last_number % 3 == 2:
        return (str(last_number-1), str(last_number), None)
