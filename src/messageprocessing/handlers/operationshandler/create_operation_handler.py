from enum import Enum
from messageprocessing.handlers.base_handler import *
from telebot.types import Message, ReplyKeyboardMarkup

from messageprocessing.handlers.base_inner_handler import BaseInnerHandler
from messageprocessing.handlers.cathegorieshandler.choose_cathegory_handler import (
    ChooseCathegoryHandler,
)
from messageprocessing.handlers.cathegorieshandler.utils import load_person_cathegories
from messageprocessing.handlers.commonhandlers.choose_option_handler import (
    ChooseOptionHandler,
)
from database.api import DatabaseApi
from database.types.cathegory import Cathegory
from database.types.operation import Operation
from messageprocessing.handlers.commonhandlers.get_number_handler import GetNumberHandler
from messageprocessing.handlers.commonhandlers.get_text_handler import GetTextHandler


class CreateOperationHandler(ReusableHandler, BaseInnerHandler):

    class State(Enum):
        WAITING_FOR_CATHEGORY = 0
        WAITING_FOR_MONEY_AMOUNT = 1
        WAITING_FOR_COMMENT = 2

    def __init__(self, outter_handler, person_id) -> None:
        BaseInnerHandler.__init__(self, outter_handler)
        self.operation = Operation()
        self.operation.person_id = person_id
        self.operation.operation_type_id = DatabaseApi().get_change_balance_operation_type_id()
        self.state = __class__.State.WAITING_FOR_CATHEGORY

    def handle_message(self, message: Message):
        assert False, "Silly mistake must be here huh"
        return self

    class ChooseOptionConstrains:
        ASKING_MESSAGE = "Выберите действие"

        OPTIONS = [
            CREATE_CATHEGORY_OPTION := "Добавить операцию",
            CHANGE_CATHEGORY_OPTION := "Откатить операцию",
            DELETE_CATHEGORY_OPTION := "Посмотреть историю",
            FINISH_OPTION := "Завершить",
        ]

    def __call_choose_cathegory_handler(self, message) -> ChooseCathegoryHandler:
        try:
            prev_state = self.state
            self.state = __class__.State.WAITING_FOR_CATHEGORY

            return ChooseCathegoryHandler.switch_to_this_handler(
                message, self, *load_person_cathegories(message.from_user.id)
            )
        except:
            self.state = prev_state
            raise

    def __call_get_money_amount_handler(self, message: Message):
        try:
            prev_state = self.state
            self.state = __class__.State.WAITING_FOR_MONEY_AMOUNT
            return GetNumberHandler.switch_to_this_handler(
                message, self, "Введите сумму операции(значение может быть отрицательным)"
            )
        except:
            self.state = prev_state
            raise

    class GetCommentConstrains:
        EMPTY_COMMENT_OPTION = "нет"
        ASKING_MESSAGE = f"Введите комментарий к операции или напишите '{EMPTY_COMMENT_OPTION}' для пустого комментария"
        MARKUP = ReplyKeyboardMarkup(
            resize_keyboard=True,
        )
        MARKUP.add(EMPTY_COMMENT_OPTION)
    
    def __call_get_comment_handler(self, message: Message):
        try:
            prev_state = self.state
            self.state = __class__.State.WAITING_FOR_COMMENT
            return GetTextHandler.switch_to_this_handler(
                message,
                self,
                __class__.GetCommentConstrains.ASKING_MESSAGE,
                markup=__class__.GetCommentConstrains.MARKUP,
                add_cancel_button=False
            )
        except:
            self.state = prev_state
            raise

    @staticmethod
    def switch_to_this_handler(message: Message, outter_handler: ReusableHandler):
        main_handler = __class__(outter_handler, message.from_user.id)
        return main_handler.__call_choose_cathegory_handler(message)

    def switch_to_existing_handler(self, message: Message):
        if self.state == __class__.State.WAITING_FOR_CATHEGORY:
            return self.got_cathegory_sh(message)
        elif self.state == __class__.State.WAITING_FOR_MONEY_AMOUNT:
            return self.got_money_amount_sh(message)
        elif self.state == __class__.State.WAITING_FOR_COMMENT:
            return self.got_comment_sh(message)

    def got_cathegory_sh(self, message: Message):
        if not self.return_result:
            return self.outter_handler.switch_to_existing_handler(message)

        self.operation.cathegory_id = self.return_result[0].id
        return self.__call_get_money_amount_handler(message)

    def got_money_amount_sh(self, message: Message):
        if not self.return_result:
            return self.outter_handler.switch_to_existing_handler(message)
        self.operation.money_amount = self.return_result
        return self.__call_get_comment_handler(message)

    def got_comment_sh(self, message: Message):
        if not self.return_result:
            return self.outter_handler.switch_to_existing_handler(message)
        if self.return_result == __class__.GetCommentConstrains.EMPTY_COMMENT_OPTION:
            self.operation.comment = ""
        else:
            self.operation.comment = self.return_result
        if not self.operation.id:
            self.operation.id = DatabaseApi().add_operation(self.operation)
        return self.outter_handler.switch_to_existing_handler(message)
