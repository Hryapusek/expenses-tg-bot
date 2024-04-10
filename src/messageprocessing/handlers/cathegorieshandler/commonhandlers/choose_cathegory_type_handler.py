from __future__ import annotations
from database.api import DatabaseApi
from handlers.base_inner_hndl import ReturningResultHandler, BaseHandler, ReusableHandler
from telebot.types import Message, ReplyKeyboardMarkup
from botstate import BotState


class ChooseCathegoryTypeHandler(ReturningResultHandler):

    CHOOSE_TYPE_MESSAGE = ("Выберите тип категории:\n"
                           "- Доходы\n"
                           "- Расходы\n")

    MARKUP = ReplyKeyboardMarkup()
    EXPENSE_CATHEGORY_BUTTON_NAME = "Расходы"
    INCOME_CATHEGORY_BUTTON_NAME = "Доходы"
    CANCEL_CATHEGORY_BUTTON_NAME = "Отменить"
    MARKUP.add(EXPENSE_CATHEGORY_BUTTON_NAME)
    MARKUP.add(INCOME_CATHEGORY_BUTTON_NAME)
    MARKUP.add(CANCEL_CATHEGORY_BUTTON_NAME)

    def handle_message(self, message: Message):
        if not message.text:
            BotState().bot.send_message(message.chat.id, __class__.CHOOSE_TYPE_MESSAGE, reply_markup=__class__.MARKUP)    
            return self
        if message.text == __class__.EXPENSE_CATHEGORY_BUTTON_NAME:
            self.outter_handler.return_result = DatabaseApi().get_expense_cathegory_type_id()
            return self.outter_handler.switch_to_existing_handler(message)
        elif message.text == __class__.INCOME_CATHEGORY_BUTTON_NAME:
            self.outter_handler.return_result = DatabaseApi().get_income_cathegory_type_id()
            return self.outter_handler.switch_to_existing_handler(message)
        elif message.text == __class__.CANCEL_CATHEGORY_BUTTON_NAME:
            self.outter_handler.return_result = None
            return self.switch_to_existing_handler(message)
        else:
            BotState().bot.send_message(message.chat.id, __class__.CHOOSE_TYPE_MESSAGE, reply_markup=__class__.MARKUP)    
            return self

    @staticmethod
    def switch_to_this_handler(message: Message, outter_handler: ReusableHandler) -> ChooseCathegoryTypeHandler:
        BotState().bot.send_message(message.chat.id, reply_markup=__class__.NA)
        return ChooseCathegoryTypeHandler(outter_handler)
