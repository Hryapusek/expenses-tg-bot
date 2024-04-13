from enum import Enum
import logging
from messageprocessing.handlers.base_handler import BaseHandler, ReusableHandler
from telebot.types import (
    Message,
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from messageprocessing.handlers.cathegorieshandler.commonhandlers.choose_cathegory_type_handler import (
    ChooseCathegoryTypeHandler,
)
from messageprocessing.handlers.commonhandlers.get_number_handler import GetNumberHandler
from messageprocessing.handlers.commonhandlers.get_text_handler import GetTextHandler
from ...botstate import BotState
from ..base_inner_handler import BaseInnerHandler, ReturningResultHandler
from database.api import DatabaseApi
from database.types.person import Person
from database.types.cathegory import Cathegory

from .constrains import *

# TODO: add cancel button everywhere


class CreateCathegoryHandler(ReturningResultHandler, ReusableHandler):

    class State(Enum):
        WAITING_FOR_TYPE = 1
        WAITING_FOR_NAME = 2
        WAITING_FOR_MONEY_LIMIT = 3
        WAITING_FOR_CURRENT_MONEY = 4
        REGISTERING_CATHEGORY = 5

    def __init__(self, outter_handler: ReusableHandler, user_id: int) -> None:
        super().__init__(outter_handler)
        self.new_cathegory = Cathegory()
        self.new_cathegory.person_id = user_id
        self.state = self.State.WAITING_FOR_TYPE

    def handle_message(self, message: Message):
        assert False, "Ahh hell naaahhh"
        return self

    @staticmethod
    def switch_to_this_handler(message: Message, outter_handler) -> BaseInnerHandler:
        this_handler = __class__(outter_handler, message.from_user.id)
        return this_handler.__call_choose_type_handler(message)

    def __call_choose_type_handler(self, message) -> ChooseCathegoryTypeHandler:
        return ChooseCathegoryTypeHandler.switch_to_this_handler(message, self)

    def __call_enter_name_handler(self, message) -> GetTextHandler:
        prev_state = self.state
        try:
            self.state = __class__.State.WAITING_FOR_NAME
            return GetTextHandler.switch_to_this_handler(
                message,
                self,
                GetNameConstrains.ASKING_MESSAGE,
                is_valid=GetNameConstrains.is_valid_name,
            )
        except:
            self.state = prev_state
            raise

    def __call_enter_money_limit_handler(self, message) -> GetNumberHandler:
        prev_state = self.state
        try:
            self.state = __class__.State.WAITING_FOR_MONEY_LIMIT
            return GetNumberHandler.switch_to_this_handler(
                message,
                self,
                GetMoneyLimitConstrains.ASKING_MESSAGE,
                GetMoneyLimitConstrains.MARKUP,
                is_valid=GetMoneyLimitConstrains.is_valid_money_limit
            )
        except:
            self.state = prev_state
            raise

    def __call_enter_current_money_handler(self, message) -> GetNumberHandler:
        prev_state = self.state
        try:
            self.state = __class__.State.WAITING_FOR_CURRENT_MONEY
            return GetNumberHandler.switch_to_this_handler(
                message,
                self,
                GetCurrentMoneyConstrains.ASKING_MESSAGE,
                GetCurrentMoneyConstrains.MARKUP,
            )
        except:
            self.state = prev_state
            raise
    
    def __register_cathegory(self, message: Message) -> GetNumberHandler:
        if not self.new_cathegory.id:
            self.new_cathegory.id = DatabaseApi().add_cathegory(self.new_cathegory)
        BotState().bot.send_message(message.chat.id, "Категория успешно создана!")
        return self.outter_handler.switch_to_existing_handler(message)

    def switch_to_existing_handler(self, message: Message) -> ReusableHandler:
        if self.state == self.State.WAITING_FOR_TYPE:
            return self.got_cathegory_type_sh(message)
        elif self.state == self.State.WAITING_FOR_NAME:
            return self.got_cathegory_name_sh(message)
        elif self.state == self.State.WAITING_FOR_MONEY_LIMIT:
            return self.got_money_limit_sh(message)
        elif self.state == self.State.WAITING_FOR_CURRENT_MONEY:
            return self.got_current_money_sh(message)
        assert False, "Something went wronk i guess..."

    def got_cathegory_type_sh(self, message) -> BaseInnerHandler:
        if not self.return_result:
            self.outter_handler.return_result = None
            return self.outter_handler.switch_to_existing_handler(message)
        self.new_cathegory.cathegory_type_id = self.return_result
        return self.__call_enter_name_handler(message)
    
    def got_cathegory_name_sh(self, message) -> BaseInnerHandler:
        if not self.return_result:
            self.outter_handler.return_result = None
            return self.outter_handler.switch_to_existing_handler(message)
        self.new_cathegory.name = self.return_result
        return self.__call_enter_money_limit_handler(message)
    
    def got_money_limit_sh(self, message) -> BaseInnerHandler:
        if not self.return_result:
            self.outter_handler.return_result = None
            return self.outter_handler.switch_to_existing_handler(message)
        self.new_cathegory.money_limit = self.return_result
        return self.__call_enter_current_money_handler(message)
    
    def got_current_money_sh(self, message) -> BaseInnerHandler:
        if not self.return_result:
            self.outter_handler.return_result = None
            return self.outter_handler.switch_to_existing_handler(message)
        self.new_cathegory.current_money = self.return_result
        return self.__register_cathegory(message)
