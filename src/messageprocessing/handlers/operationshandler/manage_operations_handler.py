from enum import Enum
from messageprocessing.handlers.base_handler import *
from telebot.types import Message

from messageprocessing.handlers.base_inner_handler import BaseInnerHandler
from messageprocessing.handlers.commonhandlers.choose_option_handler import (
    ChooseOptionHandler,
)
from database.api import DatabaseApi
from database.types.cathegory import Cathegory


class OperationsMainMenuHandler(ReusableHandler, BaseInnerHandler):

    class State(Enum):
        WAITING_FOR_OPTION = 0
        OTHER = 1

    def __init__(self, outter_handler) -> None:
        BaseInnerHandler.__init__(self, outter_handler)
        self.state = __class__.State.WAITING_FOR_OPTION

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

    def __call_choose_option_handler(self, message: Message):
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

    @staticmethod
    def switch_to_this_handler(message: Message, outter_handler: ReusableHandler):
        main_handler = CathegoriesMainMenuHandler(outter_handler)
        return main_handler.__call_choose_option_handler(message)

    def switch_to_existing_handler(self, message: Message):
        if self.state == __class__.State.OTHER:
            return self.other_sh(message)
        elif self.state == __class__.State.WAITING_FOR_OPTION:
            return self.got_option_sh(message)

    def other_sh(self, message: Message):
        return self.__call_choose_option_handler(message)

    def got_option_sh(self, message: Message):
        choosed_option = self.return_result[1]
        if choosed_option == __class__.ChooseOptionConstrains.CREATE_CATHEGORY_OPTION:
            return self.__call_create_cathegory_handler(message)
        elif choosed_option == __class__.ChooseOptionConstrains.CHANGE_CATHEGORY_OPTION:
            return self.__call_change_cathegory_handler(message)
        elif choosed_option == __class__.ChooseOptionConstrains.DELETE_CATHEGORY_OPTION:
            return self.__call_delete_cathegory_handler(message)
        elif choosed_option == __class__.ChooseOptionConstrains.FINISH_OPTION:
            return self.outter_handler.switch_to_existing_handler(message)
        assert False, "This can not be reached. Incorrect option handling?"

    def load_data_from_database(self, message: Message):
        self.income_cathegories, self.expense_cathegories = load_person_cathegories(
            message.from_user.id
        )
