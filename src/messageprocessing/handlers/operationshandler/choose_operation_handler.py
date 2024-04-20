from enum import Enum
from database.api import DatabaseApi
from database.types.cathegory import Cathegory
from database.types.operation import Operation
from messageprocessing.botstate.bot_state import BotState
from messageprocessing.handlers.base_handler import ReusableHandler
from messageprocessing.handlers.cathegorieshandler.choose_cathegory_handler import ChooseCathegoryHandler
from messageprocessing.handlers.cathegorieshandler.utils import load_person_cathegories
from messageprocessing.handlers.commonhandlers.get_number_handler import GetNumberHandler
from ..base_inner_handler import ReturningResultHandler
from telebot.types import Message, ReplyKeyboardMarkup
from .utils import operation_to_str


class ChooseOperationHandler(ReturningResultHandler, ReusableHandler):
    CHOOSE_OPERATION_MESSAGE = "\n\nВведите номер операции"
    BAD_NUMBER_MESSAGE = "Введите корректный номер операции"

    class State(Enum):
        WAITING_FOR_CATHEGORY = 0
        WAITING_FOR_OPERATION = 1

    def __init__(
        self,
        outter_handler: ReusableHandler,
    ) -> None:
        super().__init__(outter_handler)
        self.state = self.State.WAITING_FOR_CATHEGORY

    def handle_message(self, message: Message):
        assert False, "This should not be called. Silly mistake maybe made???"
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

    def __call_choose_operation_handler(self, message: Message) -> ChooseCathegoryHandler:
        try:
            prev_state = self.state
            self.state = __class__.State.WAITING_FOR_OPERATION
            self.operations = DatabaseApi().get_person_all_operations_by_ids(message.from_user.id, self.cathegory.id)
            self.operations.sort(key=lambda op: op.date, reverse=True)
            self.operations = self.operations[:5]
            if len(self.operations) == 0:
                BotState().bot.send_message(message.from_user.id, "В этой категории нет операций")
                return self.__call_choose_cathegory_handler(message)
            operations_str = "\n\n".join([f"{i+1}. {operation_to_str(op)}" for i, op in enumerate(self.operations)])
            asking_message = operations_str + "\n\nВведите номер операции из списка"
            markup = ReplyKeyboardMarkup()
            for triple in _generate_triples(len(self.operations)):
                markup.add(*filter(None, triple))
            def is_valid(number: int):
                return 1 <= number <= len(self.operations)
            return GetNumberHandler.switch_to_this_handler(message, self, asking_message, markup, is_valid)
        except:
            self.state = prev_state
            raise

    def switch_to_existing_handler(self, message: Message) -> ReusableHandler:
        if self.state == self.State.WAITING_FOR_CATHEGORY:
            return self.got_cathegory_sh(message, self.outter_handler)
        elif self.state == self.State.WAITING_FOR_OPERATION:
            return self.got_operation_sh(message, self.outter_handler)
        assert False, "This should not be called. Silly mistake maybe made???"

    def got_cathegory_sh(self, message: Message):
        if not self.return_result:
            return self.outter_handler.switch_to_existing_handler(message)
        self.cathegory: Cathegory = self.return_result[0]
        return self.__call_choose_operation_handler(message)
    
    def got_operation_sh(self, message: Message):
        if not self.return_result:
            self.outter_handler.return_result = None
            return self.outter_handler.switch_to_existing_handler(message)
        self.outter_handler.return_result: Operation = self.operations[self.return_result - 1]
        return self.outter_handler.switch_to_existing_handler(message)

    @staticmethod
    def switch_to_this_handler(
        message: Message,
        outter_handler,
    ):
        """
        return_result:
            - None if canceled
            - Operation otherwise
        """
        handler = __class__(outter_handler)
        return handler.__call_choose_cathegory_handler(message)


def _generate_triples(last_number: int):
    for i in range(1, (last_number) // 3 + 1):
        yield (str(i), str(i + 1), str(i + 2))

    if last_number % 3 == 1:
        yield (str(last_number), None, None)
    elif last_number % 3 == 2:
        yield (str(last_number - 1), str(last_number), None)
