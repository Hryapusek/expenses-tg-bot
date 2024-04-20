from enum import Enum
from messageprocessing.botstate.bot_state import BotState
from messageprocessing.handlers.base_handler import *
from telebot.types import Message

from messageprocessing.handlers.base_inner_handler import (
    BaseInnerHandler,
    ReturningResultHandler,
)
from messageprocessing.handlers.commonhandlers.choose_option_handler import (
    ChooseOptionHandler,
)
from database.api import DatabaseApi
from database.types.cathegory import Cathegory
from messageprocessing.handlers.operationshandler.choose_operation_handler import (
    ChooseOperationHandler,
)
from messageprocessing.handlers.operationshandler.create_operation_handler import (
    CreateOperationHandler,
)


class RollbackOperationHandler(ReturningResultHandler):

    class State(Enum):
        WAITING_FOR_OPERATION = 0
        WAITING_FOR_CONFIRMATION = 1

    def __init__(self, outter_handler) -> None:
        BaseInnerHandler.__init__(self, outter_handler)
        self.state = __class__.State.WAITING_FOR_OPERATION

    def handle_message(self, message: Message):
        assert False, "Silly mistake must be here huh"
        return self

    def __call_choose_operation_handler(self, message: Message):
        try:
            prev_state = self.state
            self.state = __class__.State.WAITING_FOR_OPERATION
            return ChooseOperationHandler.switch_to_this_handler(
                message,
                self,
            )
        except:
            self.state = prev_state
            raise

    def __call_confirm_operation_handler(self, message: Message):
        try:
            prev_state = self.state
            self.state = __class__.State.WAITING_FOR_CONFIRMATION
            return ChooseOptionHandler.switch_to_this_handler(
                message, self, "Вы уверены что хотите откатить операцию?", ["Да", "Нет"]
            )
        except:
            self.state = prev_state
            raise

    @staticmethod
    def switch_to_this_handler(message: Message, outter_handler: ReusableHandler):
        main_handler = __class__(outter_handler)
        return main_handler.__call_choose_operation_handler(message)

    def switch_to_existing_handler(self, message: Message):
        if self.state == __class__.State.WAITING_FOR_OPERATION:
            return self.got_operation_sh(message)
        elif self.state == __class__.State.WAITING_FOR_CONFIRMATION:
            return self.got_confirmation_sh(message)

    def got_operation_sh(self, message: Message):
        if not self.return_result:
            return self.outter_handler.switch_to_existing_handler(message)
        self.operation = self.return_result
        return self.__call_confirm_operation_handler(message)

    def got_confirmation_sh(self, message: Message):
        if not self.return_result:
            return self.outter_handler.switch_to_existing_handler(message)
        choosed_option = self.return_result[1]
        if choosed_option == "Да":
            DatabaseApi.rollback_operation(self.operation)
            BotState().bot.send_message(message.chat.id, "Операция успешно отменена")
        return self.outter_handler.switch_to_existing_handler(message)
