from enum import Enum

import telebot
from telebot.types import Message

from src.database.types.cathegory import Cathegory
from .base_inner_handler import BaseInnerHandler
from .cathegorieshandler.change_cathegory_handler import ChangeCathegoryHandler
from .cathegorieshandler.create_cathegory_handler import CreateCathegoryHandler
from .cathegorieshandler.delete_cathegory_hanlder import DeleteCathegoryHandler
from .commonhandlers.choose_option_handler import ChooseOptionHandler
from ..botstate import BotState


class MainMenuHandler(BaseInnerHandler):
    class State(Enum):
        WAITING_FOR_OPTION = 0
        OTHER = 1

    class ChooseOptionConstrains:
        ASKING_MESSAGE = "Выберите действие"

        OPTIONS = [
            CREATE_CATHEGORY_OPTION := "Создать категорию",
            CHANGE_CATHEGORY_OPTION := "Изменить категорию",
            DELETE_CATHEGORY_OPTION := "Удалить категорию"
        ]

    def __init__(self, outter_handler=None):
        BaseInnerHandler.__init__(self, None)
        self.income_cathegories: list[Cathegory] = []
        self.expense_cathegories: list[Cathegory] = []
        self.state = self.State.WAITING_FOR_OPTION

    MARKUP = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in ChooseOptionConstrains.OPTIONS:
        MARKUP.add(i)
    GREETING_MESSAGE = "Что вы хотите сделать?"

    def __call_create_cathegory_handler(self, message: Message):
        try:
            prev_state = self.state
            self.state = __class__.State.OTHER
            return CreateCathegoryHandler.switch_to_this_handler(message, self)
        except:
            self.state = prev_state
            raise

    def __call_change_cathegory_handler(self, message: Message):
        try:
            prev_state = self.state
            self.state = __class__.State.OTHER
            return ChangeCathegoryHandler.switch_to_this_handler(
                message, self, self.income_cathegories, self.expense_cathegories
            )
        except:
            self.state = prev_state
            raise

    def __call_delete_cathegory_handler(self, message: Message):
        try:
            prev_state = self.state
            self.state = __class__.State.OTHER
            return DeleteCathegoryHandler.switch_to_this_handler(
                message, self, self.income_cathegories, self.expense_cathegories
            )
        except:
            self.state = prev_state
            raise

    def __call_choose_option_handler(self, message: Message):
        try:
            prev_state = self.state
            self.state = __class__.State.WAITING_FOR_OPTION
            return ChooseOptionHandler.switch_to_this_handler(
                message,
                self,
            )
        except:
            self.state = prev_state
            raise

    def handle_message(self, message: Message):
        if message.text == self.ChooseOptionConstrains.CREATE_CATHEGORY_OPTION:
            return self.__call_create_cathegory_handler(message)
        elif message.text == self.ChooseOptionConstrains.CHANGE_CATHEGORY_OPTION:
            return self.__call_change_cathegory_handler(message)
        elif message.text == self.ChooseOptionConstrains.DELETE_CATHEGORY_OPTION:
            return self.__call_delete_cathegory_handler(message)
        return self

    @staticmethod
    def switch_to_this_handler(message: Message, outter_handler=None):
        BotState().bot.send_message(message.chat.id, __class__.GREETING_MESSAGE, reply_markup=__class__.MARKUP)
        return MainMenuHandler()

    def switch_to_existing_handler(self, message: Message):
        self.switch_to_this_handler(message)
        return self
