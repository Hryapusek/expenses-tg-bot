from enum import Enum

from psycopg2 import ProgrammingError
from messageprocessing.handlers.base_handler import ReusableHandler
from telebot.types import (
    Message,
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from messageprocessing.handlers.commonhandlers.get_number_handler import GetNumberHandler
from messageprocessing.handlers.commonhandlers.get_text_handler import GetTextHandler

from .cathegorieshandler.manage_cathegories_handler import CathegoriesMainMenuHandler
from ..botstate import BotState
from .base_inner_handler import BaseInnerHandler
from database.api import DatabaseApi
from database.types.person import Person


class CreateUserHandler(ReusableHandler, BaseInnerHandler):

    class State(Enum):
        WAITING_FOR_NAME = 1
        WAITING_FOR_BALANCE = 2

    def __init__(self, outter_handler: ReusableHandler, user_id) -> None:
        super().__init__(outter_handler)
        self.state = __class__.State.WAITING_FOR_NAME
        self.person = Person()
        self.person.id = user_id

    def handle_message(self, message: Message):
        assert False, "Silly mistake must be made huh..."
        return self

    class GetNameConstrains:
        ASKING_MESSAGE = "Введите имя для вашего пользователя"

        def is_valid_name(name: str) -> tuple[bool, str]:
            if len(name) > 200:
                return (False, "Имя слишком длинное. Попробуйте снова")
            return (True, "")

    def __call_get_name_handler(self, message: Message):
        try:
            prev_state = self.state
            self.state = __class__.State.WAITING_FOR_NAME
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(message.from_user.username)
            return GetTextHandler.switch_to_this_handler(
                message,
                self,
                __class__.GetNameConstrains.ASKING_MESSAGE,
                markup=markup,
                is_valid=__class__.GetNameConstrains.is_valid_name,
                add_cancel_button=False,
            )
        except:
            self.state = prev_state
            raise

    class GetBalanceConstrains:
        ASKING_MESSAGE = (
            "Теперь разберемся с вашим текущим балансом. "
            "Какую сумму хотели бы иметь? Введите целое число."
            )
        MARKUP = ReplyKeyboardMarkup(resize_keyboard=True)
        for button1, button2 in [
            ("0", "10000"),
            ("20000", "30000"),
            ("40000", "50000"),
        ]:
            MARKUP.add(button1, button2)

    def __call_get_balance_handler(self, message: Message):
        try:
            prev_state = self.state
            self.state = __class__.State.WAITING_FOR_BALANCE
            return GetNumberHandler.switch_to_this_handler(
                message,
                self,
                __class__.GetBalanceConstrains.ASKING_MESSAGE,
                markup=__class__.GetBalanceConstrains.MARKUP,
                add_cancel_button=False
            )
        except:
            self.state = prev_state
            raise

    GREETING_MESSAGE = "Давайте перейдем к созданию вашего нового профиля."

    def switch_to_existing_handler(self, message: Message) -> ReusableHandler:
        if self.state == __class__.State.WAITING_FOR_NAME:
            return self.got_name_sh(message)
        elif self.state == __class__.State.WAITING_FOR_BALANCE:
            return self.got_balance_sh(message)

    def got_name_sh(self, message: Message):
        self.person.name = self.return_result
        return self.__call_get_balance_handler(message)
    
    def got_balance_sh(self, message: Message):
        self.person.balance = self.return_result
        try:
            DatabaseApi().add_person(self.person)
        except ProgrammingError:
            pass
        BotState().bot.send_message(
            message.chat.id,
            "С регистрацией успешно завершили. Предлагаю теперь настроить категории.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return CathegoriesMainMenuHandler.switch_to_this_handler(message, self.outter_handler)

    @staticmethod
    def switch_to_this_handler(message: Message, outter_handler: ReusableHandler):
        BotState().bot.send_message(
            message.chat.id,
            __class__.GREETING_MESSAGE,
            reply_markup=ReplyKeyboardRemove(),
        )
        handler = __class__(outter_handler, message.from_user.id)
        return handler.__call_get_name_handler(message)
