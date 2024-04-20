from enum import Enum

import telebot
from database.api import DatabaseApi
from database.types.person import Person
from messageprocessing.botstate.bot_state import BotState
from messageprocessing.handlers.base_handler import BaseHandler
from telebot.types import Message
from messageprocessing.handlers.base_inner_handler import BaseInnerHandler
from messageprocessing.handlers.cathegorieshandler.manage_cathegories_handler import CathegoriesMainMenuHandler
from messageprocessing.handlers.commonhandlers.choose_option_handler import ChooseOptionHandler
from messageprocessing.handlers.operationshandler.manage_operations_handler import OperationsMainMenuHandler

from database.types.cathegory import Cathegory


class MainMenuHandler(BaseInnerHandler):
    class State(Enum):
        WAITING_FOR_OPTION = 0
        IN_CATHEGORIES_MAIN_MENU = 1
        IN_OPERATIONS_MAIN_MENU = 2

    def __init__(self, outter_handler=None):
        BaseInnerHandler.__init__(self, None)
        self.state = self.State.WAITING_FOR_OPTION

    def handle_message(self, message) -> BaseHandler:
        assert False, "This method is not implemented"
        return self

    def __call_manage_cathegories_handler(self, message: Message):
        try:
            prev_state = self.state
            self.state = __class__.State.IN_CATHEGORIES_MAIN_MENU
            return CathegoriesMainMenuHandler.switch_to_this_handler(message, self)
        except:
            self.state = prev_state
            raise

    def __call_manage_operations_handler(self, message: Message):
        try:
            prev_state = self.state
            self.state = __class__.State.IN_OPERATIONS_MAIN_MENU
            return OperationsMainMenuHandler.switch_to_this_handler(message, self)
        except:
            self.state = prev_state
            raise

    class ChooseOptionConstrains:
        ASKING_MESSAGE = "Выберите действие"

        OPTIONS = [
            CHECK_CATHEGORIES_OPTION := "Категории",
            CHECK_OPERATIONS_OPTION := "Операции",
        ]

    def __call_choose_option_handler(self, message: Message):
        try:
            prev_state = self.state
            person: Person = DatabaseApi().get_person_by_id(message.from_user.id)
            GREETING_MESSAGE = (f"Рад снова вас видеть, {person.name}!\n"
                                f"Ваш баланс: {person.balance}\n\n"
                                )
            self.state = __class__.State.WAITING_FOR_OPTION
            return ChooseOptionHandler.switch_to_this_handler(
                message,
                self,
                GREETING_MESSAGE + self.ChooseOptionConstrains.ASKING_MESSAGE,
                self.ChooseOptionConstrains.OPTIONS,
                add_cancel_option=False
            )
        except:
            self.state = prev_state
            raise

    @staticmethod
    def switch_to_this_handler(message: Message, outter_handler=None):
        handler = __class__()
        return handler.__call_choose_option_handler(message)

    def switch_to_existing_handler(self, message: Message):
        if self.state == self.State.IN_CATHEGORIES_MAIN_MENU:
            return self.finished_cathegories_sh(message)
        elif self.state == self.State.IN_OPERATIONS_MAIN_MENU:
            return self.finished_operations_sh(message)
        elif self.state == self.State.WAITING_FOR_OPTION:
            return self.got_option_sh(message)
        assert False, "State is not defined"

    def got_option_sh(self, message: Message):
        if message.text == self.ChooseOptionConstrains.CHECK_CATHEGORIES_OPTION:
            return self.__call_manage_cathegories_handler(message)
        elif message.text == self.ChooseOptionConstrains.CHECK_OPERATIONS_OPTION:
            return self.__call_manage_operations_handler(message)
        assert False, "Option is not defined"

    def finished_cathegories_sh(self, message: Message):
        return self.__call_choose_option_handler(message)

    def finished_operations_sh(self, message: Message):
        return self.__call_choose_option_handler(message)
