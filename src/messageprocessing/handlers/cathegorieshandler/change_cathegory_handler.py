from __future__ import annotations
from enum import Enum
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


class ChangeCathegoryHandler(ReusableHandler, BaseInnerHandler):

    class State(Enum):
        WAITING_FOR_CATHEGORY = 0
        WAITING_FOR_OPTION = 1
        WAITING_FOR_NAME = 2
        WAITING_FOR_TYPE = 3
        WAITING_FOR_CURRENT_MONEY = 4
        WAITING_FOR_LIMIT = 5

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
        if self.state == __class__.State.WAITING_FOR_OPTION:
            return self.got_option_sh(message)
        elif self.state == __class__.State.WAITING_FOR_CATHEGORY:
            return self.got_cathegory_sh(message)
        elif self.state == __class__.State.WAITING_FOR_NAME:
            return self.got_name_sh(message)
        elif self.state == __class__.State.WAITING_FOR_TYPE:
            return self.got_type_sh(message)
        elif self.state == __class__.State.WAITING_FOR_CURRENT_MONEY:
            return self.got_current_money_sh(message)
        elif self.state == __class__.State.WAITING_FOR_LIMIT:
            return self.got_limit_sh(message)

    class ChooseOptionConstrains:
        ASKING_MESSAGE = "Выберите что хотите изменить"
        OPTIONS = [
            NAME_OPTION := "Название",
            TYPE_OPTION := "Тип",
            CURRENT_MONEY_OPTION := "Текущие траты",
            LIMIT_OPTION := "Лимит",
            CHANGE_CATHEGORY_OPTION := "Поменять категорию",
            FINISH_OPTION := "Завершить",
        ]

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

    def __call_choose_option_handler(self, message) -> ChooseOptionHandler:
        try:
            prev_state = self.state
            self.state = __class__.State.WAITING_FOR_OPTION
            return ChooseOptionHandler.switch_to_this_handler(
                message,
                self,
                __class__.ChooseOptionConstrains.ASKING_MESSAGE,
                __class__.ChooseOptionConstrains.OPTIONS,
                add_cancel_option=False,
            )
        except:
            self.state = prev_state
            raise

    class ChangeNameConstrains:
        ASKING_MESSAGE = "Выберите новое название для категории"

    def __call_change_name_handler(self, message) -> GetTextHandler:
        try:
            prev_state = self.state
            self.state = __class__.State.WAITING_FOR_NAME
            return GetTextHandler.switch_to_this_handler(
                message,
                self,
                __class__.ChangeNameConstrains.ASKING_MESSAGE,
            )
        except:
            self.state = prev_state
            raise

    def __call_change_type_handler(self, message) -> ChooseCathegoryTypeHandler:
        try:
            prev_state = self.state
            self.state = __class__.State.WAITING_FOR_TYPE
            return ChooseCathegoryTypeHandler.switch_to_this_handler(
                message,
                self,
            )
        except:
            self.state = prev_state
            raise

    def __call_change_current_money_handler(self, message) -> GetNumberHandler:
        try:
            prev_state = self.state
            self.state = __class__.State.WAITING_FOR_CURRENT_MONEY
            return GetNumberHandler.switch_to_this_handler(
                message,
                self,
                GetMoneyLimitConstrains.ASKING_MESSAGE,
                GetMoneyLimitConstrains.MARKUP,
                is_valid=GetMoneyLimitConstrains.is_valid_money_limit,
            )
        except:
            self.state = prev_state
            raise

    def __call_change_limit_handler(self, message) -> GetNumberHandler:
        try:
            prev_state = self.state
            self.state = __class__.State.WAITING_FOR_LIMIT
            return GetNumberHandler.switch_to_this_handler(
                message,
                self,
                GetCurrentMoneyConstrains.ASKING_MESSAGE,
                GetCurrentMoneyConstrains.MARKUP,
            )
        except:
            self.state = prev_state
            raise

    def got_option_sh(self, message: Message):
        choosed_option = self.return_result[1]
        if choosed_option == __class__.ChooseOptionConstrains.FINISH_OPTION:
            return self.outter_handler.switch_to_existing_handler(message)
        elif choosed_option == __class__.ChooseOptionConstrains.NAME_OPTION:
            return self.__call_change_name_handler(message)
        elif choosed_option == __class__.ChooseOptionConstrains.TYPE_OPTION:
            return self.__call_change_type_handler(message)
        elif choosed_option == __class__.ChooseOptionConstrains.CURRENT_MONEY_OPTION:
            return self.__call_change_current_money_handler(message)
        elif choosed_option == __class__.ChooseOptionConstrains.LIMIT_OPTION:
            return self.__call_change_limit_handler(message)
        elif choosed_option == __class__.ChooseOptionConstrains.CHANGE_CATHEGORY_OPTION:
            return self.__call_choose_cathegory_handler(message)
        elif choosed_option == __class__.ChooseOptionConstrains.FINISH_OPTION:
            return self.outter_handler.switch_to_existing_handler(message)

    def got_cathegory_sh(self, message: Message):
        if not self.return_result:
            return self.outter_handler.switch_to_existing_handler(message)
        self.cathegory: Cathegory = self.return_result[0]
        self.cathegory_type_array = self.return_result[1]
        self.cathegory_index = self.return_result[2]
        self.__show_cathegory(message)
        return self.__call_choose_option_handler(message)

    def got_name_sh(self, message: Message):
        if not self.return_result:
            self.__show_cathegory(message)
            return self.__call_choose_option_handler(message)
        old_cathegory = self.cathegory
        self.cathegory.name = self.return_result
        self.__update_cathegory(message, old_cathegory)
        self.__show_cathegory(message)
        return self.__call_choose_option_handler(message)

    def got_type_sh(self, message: Message):
        if not self.return_result:
            self.__show_cathegory(message)
            return self.__call_choose_option_handler(message)
        old_cathegory = self.cathegory
        self.cathegory.cathegory_type_id = self.return_result
        self.__update_cathegory(message, old_cathegory)
        self.__show_cathegory(message)
        return self.__call_choose_option_handler(message)

    def got_current_money_sh(self, message: Message):
        if not self.return_result:
            self.__show_cathegory(message)
            return self.__call_choose_option_handler(message)
        old_cathegory = self.cathegory
        self.cathegory.current_money = self.return_result
        self.__update_cathegory(message, old_cathegory)
        self.__show_cathegory(message)
        return self.__call_choose_option_handler(message)
    
    def got_limit_sh(self, message: Message):
        if not self.return_result:
            self.__show_cathegory(message)
            return self.__call_choose_option_handler(message)
        old_cathegory = self.cathegory
        self.cathegory.money_limit = self.return_result
        self.__update_cathegory(message, old_cathegory)
        self.__show_cathegory(message)
        return self.__call_choose_option_handler(message)

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

    def __update_cathegory(self, message: Message, old_cathegory):
        try:
            DatabaseApi().update_cathegory(self.cathegory)
        except Exception:
            self.cathegory = old_cathegory
            try:
                BotState().bot.send_message(
                    message.chat.id, "Не удалось сохранить категорию."
                )
            except:
                pass
            raise
