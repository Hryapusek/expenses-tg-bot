from __future__ import annotations
from enum import Enum

from psycopg2 import ProgrammingError
from database.api import DatabaseApi
from database.types.cathegory import Cathegory
from messageprocessing.botstate.bot_state import BotState
from messageprocessing.handlers.base_handler import BaseHandler
from messageprocessing.handlers.base_inner_handler import BaseInnerHandler
from messageprocessing.handlers.cathegorieshandler.commonhandlers.choose_cathegory_type_handler import (
    ChooseCathegoryTypeHandler,
)
from messageprocessing.handlers.cathegorieshandler.constrains import *
from messageprocessing.handlers.commonhandlers.choose_option_handler import (
    ChooseOptionHandler,
)
from messageprocessing.handlers.commonhandlers.get_number_handler import (
    GetNumberHandler,
)
from messageprocessing.handlers.commonhandlers.get_text_handler import GetTextHandler
from ..base_handler import ReusableHandler
from telebot.types import Message
from .choose_cathegory_handler import ChooseCathegoryHandler


class DeleteCathegoryHandler(ReusableHandler, BaseInnerHandler):

    class State(Enum):
        WAITING_FOR_CATHEGORY = 0
        WAITING_FOR_CONFIRMATION = 1

    def __init__(
        self,
        outter_handler: BaseInnerHandler,
        income_cathegories: list[Cathegory],
        expense_cathegories: list[Cathegory],
    ) -> None:
        super().__init__(outter_handler)
        self.state = __class__.State.WAITING_FOR_CATHEGORY
        self.income_cathegories = income_cathegories
        self.expense_cathegories = expense_cathegories

    def handle_message(self, message: Message):
        if not message.text:
            return self

        return self

    @staticmethod
    def switch_to_this_handler(
        message: Message,
        outter_handler,
        income_cathegories: list[Cathegory],
        expense_cathegories: list[Cathegory],
    ):
        this_handler = __class__(outter_handler, income_cathegories, expense_cathegories)
        return this_handler.__call_choose_cathegory_handler(message)

    def switch_to_existing_handler(self, message: Message):
        if self.state == __class__.State.WAITING_FOR_CONFIRMATION:
            return self.got_confirmation_sh(message)
        elif self.state == __class__.State.WAITING_FOR_CATHEGORY:
            return self.got_cathegory_sh(message)

    def __call_choose_cathegory_handler(self, message) -> ChooseCathegoryHandler:
        try:
            prev_state = self.state
            self.state = __class__.State.WAITING_FOR_CATHEGORY
            return ChooseCathegoryHandler.switch_to_this_handler(
            message, self, self.income_cathegories, self.expense_cathegories
        )
        except:
            self.state = prev_state
            raise

    class ConfirmationConstrains:
        ASKING_MESSAGE = "Вы уверены что хотите удалить эту категорию?"
        OPTIONS = [
            YES_OPTION := "Да",
            NO_OPTION := "Нет",
        ]

    def __call_confirmation_handler(self, message) -> ChooseOptionHandler:
        try:
            prev_state = self.state
            self.state = __class__.State.WAITING_FOR_CONFIRMATION
            self.__show_cathegory(message)
            return ChooseOptionHandler.switch_to_this_handler(
                message,
                self,
                __class__.ConfirmationConstrains.ASKING_MESSAGE,
                __class__.ConfirmationConstrains.OPTIONS,
                add_cancel_option=True,
            )
        except:
            self.state = prev_state
            raise

    def got_confirmation_sh(self, message: Message):
        choosed_option = self.return_result
        if not choosed_option or choosed_option == __class__.ConfirmationConstrains.NO_OPTION:
            return self.__call_choose_cathegory_handler
        if choosed_option == __class__.ConfirmationConstrains.YES_OPTION:
            try:
                DatabaseApi().remove_cathegory_by_id(self.cathegory.id)
                del self.cathegory_type_array[self.cathegory_index]
            except ProgrammingError:
                pass
            BotState().bot.send_message(message.chat.id, "Категория была успешно удалена!")
            return self.__call_choose_cathegory_handler(message)
        assert False, "Bro HOW dogggg"

    def got_cathegory_sh(self, message: Message):
        if not self.return_result:
            return self.outter_handler.switch_to_existing_handler(message)
        self.cathegory: Cathegory = self.return_result[0]
        self.cathegory_type_array = self.return_result[1]
        self.cathegory_index = self.return_result[2]
        self.__show_cathegory(message)
        return self.__call_confirmation_handler(message)

    def __show_cathegory(self, message: Message):
        line_format = "Название: {}\n" "Тип: {}\n" "Текущие траты: {:,}\n" "Лимит: {:,}"
        result_str = line_format.format(
            self.cathegory.name,
            (
                "Расходы"
                if self.cathegory.cathegory_type_id
                == DatabaseApi().get_expense_cathegory_type_id()
                else "Доходы"
            ),
            self.cathegory.current_money,
            self.cathegory.money_limit,
        )
        BotState().bot.send_message(message.chat.id, result_str)
