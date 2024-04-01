from messageprocessing.handlers.base_hndl import *
from telebot.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

from messageprocessing.handlers.cathegorieshandler.create_cathegory_handler import CreateCathegoryHandler
from ...botstate import BotState
from database.api import DatabaseApi
from database.types.person import Person
from database.types.cathegory import Cathegory


class ManageCathegoriesHandler(BaseHandler):

    def handle_message(self, message: Message):
        return self

    @staticmethod
    def switch_to_this_handler(message: Message):
        handler = CathegoriesMainMenuHandler.switch_to_this_handler(
            message
        )
        return handler


class CathegoriesMainMenuHandler(ReusableHandler):
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

    def __init__(self) -> None:
        self.person: Person = None
        self.cathegories: list[Cathegory] = []

    def handle_message(self, message: Message):
        if not message.text:
            return self
        if message.text == __class__.CREATE_CATHEGORY_BUTTON_NAME:
            return CreateCathegoryHandler.switch_to_this_handler(message, self)
        return self
        pass

    @staticmethod
    def switch_to_this_handler(message: Message):
        handler = CathegoriesMainMenuHandler()
        handler.load_data_from_database(message)
        result = ""
        cathegories_str = handler.cathegories_to_string()
        result += cathegories_str + __class__.CHOOSE_OPTION_MESSAGE
        BotState().bot.send_message(message.chat.id, result, reply_markup=__class__.MARKUP)
        return handler
    
    def switch_to_existing_handler(self, message: Message):
        result = ""
        cathegories_str = self.cathegories_to_string()
        result += cathegories_str + __class__.CHOOSE_OPTION_MESSAGE
        BotState().bot.send_message(message.chat.id, result, reply_markup=__class__.MARKUP)
        return self

    def load_data_from_database(self, message: Message):
        self.cathegories = DatabaseApi().get_person_all_cathegories_by_id(message.from_user.id)

    def cathegories_to_string(self) -> str:
        if len(self.cathegories) == 0:
            return "Нам не удалось найти ни одной вашей категории."
        result = ""
        line_format = ("{}. {}\n"
                       "\tБаланс: {:,}\n"
                       "\tЛимит: {:,}")
        income_cathegories = filter(lambda x: x.cathegory_type_id == DatabaseApi().get_income_cathegory_type_id(), 
                                    self.cathegories)
        expense_cathegories = filter(lambda x: x.cathegory_type_id == DatabaseApi().get_expense_cathegory_type_id(), 
                                    self.cathegories)
        start_number = 1
        for cathegory_type_name, cathegory in (("Доходные категории", income_cathegories),
                                               ("Расходные категории", expense_cathegories)):
            result += cathegory_type_name + ":\n"
            for seq_no, cathegory in enumerate(self.cathegories, start_number):
                line = line_format.format(seq_no, cathegory.name, cathegory.current_money, cathegory.money_limit)
                result += line + '\n'
                start_number = seq_no
            result += '\n\n'
        return result
