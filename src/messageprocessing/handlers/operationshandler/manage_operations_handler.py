from enum import Enum
from messageprocessing.handlers.base_handler import *
from telebot.types import Message

from messageprocessing.handlers.base_inner_handler import BaseInnerHandler
from messageprocessing.handlers.commonhandlers.choose_option_handler import (
    ChooseOptionHandler,
)
from database.api import DatabaseApi
from database.types.cathegory import Cathegory
from messageprocessing.handlers.operationshandler.create_operation_handler import CreateOperationHandler
from messageprocessing.handlers.operationshandler.history_of_operation_handler import HistoryOfOperationsHandler
from messageprocessing.handlers.operationshandler.rollback_operation_handler import RollbackOperationHandler


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
            CREATE_OPERATION_OPTION := "Добавить операцию",
            ROLLBACK_OPERATION_OPTION := "Откатить операцию",
            OPERATION_HISTORY_OPTION := "Посмотреть историю",
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

    def __call_create_operation_handler(self, message: Message):
        try:
            prev_state = self.state
            self.state = __class__.State.OTHER
            return CreateOperationHandler.switch_to_this_handler(message, self)
        except:
            self.state = prev_state
            raise

    def __call_rollback_operation_handler(self, message: Message):
        try:
            prev_state = self.state
            self.state = __class__.State.OTHER
            return RollbackOperationHandler.switch_to_this_handler(message, self)
        except:
            self.state = prev_state
            raise

    def __call_operation_history_handler(self, message: Message):
        try:
            prev_state = self.state
            self.state = __class__.State.OTHER
            return HistoryOfOperationsHandler.switch_to_this_handler(message, self)
        except:
            self.state = prev_state
            raise

    @staticmethod
    def switch_to_this_handler(message: Message, outter_handler: ReusableHandler):
        main_handler = __class__(outter_handler)
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
        if choosed_option == __class__.ChooseOptionConstrains.CREATE_OPERATION_OPTION:
            return self.__call_create_operation_handler(message)
        elif choosed_option == __class__.ChooseOptionConstrains.ROLLBACK_OPERATION_OPTION:
            return self.__call_rollback_operation_handler(message)
        elif choosed_option == __class__.ChooseOptionConstrains.OPERATION_HISTORY_OPTION:
            return self.__call_operation_history_handler(message)
        elif choosed_option == __class__.ChooseOptionConstrains.FINISH_OPTION:
            return self.outter_handler.switch_to_existing_handler(message)
        assert False, "This can not be reached. Incorrect option handling?"
