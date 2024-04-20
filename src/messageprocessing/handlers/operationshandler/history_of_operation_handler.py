from enum import Enum
from messageprocessing.botstate.bot_state import BotState
from messageprocessing.handlers.base_handler import *
from telebot.types import Message

from messageprocessing.handlers.base_inner_handler import (
    BaseInnerHandler,
    ReturningResultHandler,
)
from messageprocessing.handlers.cathegorieshandler.choose_cathegory_handler import ChooseCathegoryHandler
from messageprocessing.handlers.cathegorieshandler.utils import load_person_cathegories
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
from messageprocessing.handlers.operationshandler.utils import operation_to_str


class HistoryOfOperationsHandler(ReturningResultHandler):

    class State(Enum):
        WAITING_FOR_CATHEGORY = 0

    def __init__(self, outter_handler) -> None:
        BaseInnerHandler.__init__(self, outter_handler)
        self.state = __class__.State.WAITING_FOR_CATHEGORY

    def handle_message(self, message: Message):
        assert False, "Silly mistake must be here huh"
        return self

    def __call_choose_cathegory_handler(self, message: Message) -> ChooseCathegoryHandler:
        try:
            prev_state = self.state
            self.state = __class__.State.WAITING_FOR_CATHEGORY
            return ChooseCathegoryHandler.switch_to_this_handler(
            message, self, *load_person_cathegories(message.from_user.id)
        )
        except:
            self.state = prev_state
            raise

    def __send_operations(self, message: Message) -> ChooseCathegoryHandler:
            self.operations = DatabaseApi().get_person_all_operations_by_ids(message.from_user.id, self.cathegory.id)
            self.operations.sort(key=lambda op: op.date, reverse=True)
            self.operations = self.operations[:5]
            if len(self.operations) == 0:
                BotState().bot.send_message(message.from_user.id, "В этой категории нет операций")
                return self.__call_choose_cathegory_handler(message)
            operations_str = "\n\n".join([f"{i+1}. {operation_to_str(op)}" for i, op in enumerate(self.operations)])
            last_5_op_str = "Ваши 5 последних операции:\n\n" + operations_str
            BotState().bot.send_message(message.from_user.id, last_5_op_str)

    @staticmethod
    def switch_to_this_handler(message: Message, outter_handler: ReusableHandler):
        main_handler = __class__(outter_handler)
        return main_handler.__call_choose_cathegory_handler(message)

    def switch_to_existing_handler(self, message: Message):
        if self.state == __class__.State.WAITING_FOR_CATHEGORY:
            return self.got_cathegory_sh(message)
        assert False, "This can not be reached. Incorrect option handling?"

    def got_cathegory_sh(self, message: Message):
        if not self.return_result:
            return self.outter_handler.switch_to_existing_handler(message)
        self.cathegory = self.return_result[0]
        self.__send_operations(message)
        return self.outter_handler.switch_to_existing_handler(message)
