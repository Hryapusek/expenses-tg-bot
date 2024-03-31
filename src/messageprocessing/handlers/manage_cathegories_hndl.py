from messageprocessing.handlers.base_hndl import BaseHandler
from telebot.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from ..botstate import BotState
from .base_inner_hndl import BaseInnerHandler
from database.api import DatabaseApi
from database.types.person import Person
from database.types.cathegory import Cathegory


class ManageCathegoriesHandler(BaseHandler):

    def __init__(self) -> None:
        self.person: Person = None
        self.cathegories: list[Cathegory] = []
        self.inner_handler: BaseHandler = None

    def handle_message(self, message: Message):
        self.inner_handler = self.inner_handler.handle_message(message)
        if self.inner_handler is None:
            # TODO: return cathegories handler
            pass
        return self

    @staticmethod
    def switch_to_this_handler(message: Message):
        handler = ManageCathegoriesHandler()
        handler.inner_handler = _CathegoriesMainMenuHandler.switch_to_this_handler(
            message, handler
        )
        return handler


class _CathegoriesMainMenuHandler(BaseInnerHandler):
    CHOOSE_OPTION_MESSAGE = "\n\nВыберите действие"

    MARKUP = ReplyKeyboardMarkup()
    CREATE_CATHEGORY_BUTTON_NAME = "Создать категорию"
    CHANGE_CATHEGORY_BUTTON_NAME = "Изменить категорию"
    DELETE_CATHEGORY_BUTTON_NAME = "Удалить категорию"
    FINISH_BUTTON_NAME = "Завершить категорию"

    MARKUP.add(CREATE_CATHEGORY_BUTTON_NAME)
    MARKUP.add(CHANGE_CATHEGORY_BUTTON_NAME)
    MARKUP.add(DELETE_CATHEGORY_BUTTON_NAME)
    MARKUP.add(FINISH_BUTTON_NAME)

    def handle_message(self, message: Message):
        pass

    @staticmethod
    def switch_to_this_handler(message: Message, outter_handler: ManageCathegoriesHandler):
        handler = _CathegoriesMainMenuHandler(outter_handler)
        handler.load_data_from_database(message)
        result = ""
        cathegories_str = handler.cathegories_to_string()
        result += cathegories_str + __class__.CHOOSE_OPTION_MESSAGE
        BotState().bot.send_message(message.chat.id, result, reply_markup=__class__.MARKUP)
        return handler

    def load_data_from_database(self, message: Message):
        self.outter_handler: ManageCathegoriesHandler
        self.outter_handler.cathegories = DatabaseApi().get_person_all_cathegories_by_id(message.from_user.id)

    def cathegories_to_string(self) -> str:
        if len(self.outter_handler.cathegories) == 0:
            return "Нам не удалось найти ни одной вашей категории."
        result = ""
        line_format = ("{}. {}\n"
                       "\tБаланс: {:,}\n"
                       "\tЛимит: {:,}")
        income_cathegories = filter(lambda x: x.cathegory_type_id == DatabaseApi().get_income_cathegory_type_id(), 
                                    self.outter_handler.cathegories)
        expense_cathegories = filter(lambda x: x.cathegory_type_id == DatabaseApi().get_expense_cathegory_type_id(), 
                                    self.outter_handler.cathegories)
        start_number = 1
        for cathegory_type_name, cathegory in (("Доходные категории", income_cathegories),
                                               ("Расходные категории", expense_cathegories)):
            result += cathegory_type_name + ":\n"
            for seq_no, cathegory in enumerate(self.outter_handler.cathegories, start_number):
                line = line_format.format(seq_no, cathegory.name, cathegory.current_money, cathegory.money_limit)
                result += line + '\n'
                start_number = seq_no
            result += '\n\n'
        return result


class _CreateCathegoryHandler(BaseInnerHandler):
    CHOOSE_OPTION_MESSAGE = "\n\nВыберите действие"

    MARKUP = ReplyKeyboardMarkup()
    CREATE_CATHEGORY_BUTTON_NAME = "Создать категорию"
    CHANGE_CATHEGORY_BUTTON_NAME = "Изменить категорию"
    DELETE_CATHEGORY_BUTTON_NAME = "Удалить категорию"
    FINISH_BUTTON_NAME = "Завершить категорию"

    MARKUP.add(CREATE_CATHEGORY_BUTTON_NAME)
    MARKUP.add(CHANGE_CATHEGORY_BUTTON_NAME)
    MARKUP.add(DELETE_CATHEGORY_BUTTON_NAME)
    MARKUP.add(FINISH_BUTTON_NAME)

    def handle_message(self, message: Message):
        pass

    @staticmethod
    def switch_to_this_handler(message: Message, outter_handler: ManageCathegoriesHandler):
        handler = _CathegoriesMainMenuHandler(outter_handler)
        handler.load_data_from_database(message)
        result = ""
        cathegories_str = handler.cathegories_to_string()
        result += cathegories_str + __class__.CHOOSE_OPTION_MESSAGE
        BotState().bot.send_message(message.chat.id, result, reply_markup=__class__.MARKUP)
        return handler
