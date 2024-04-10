from messageprocessing.handlers.base_hndl import *
from telebot.types import Message

from messageprocessing.handlers.cathegorieshandler.change_cathegory_handler import ChangeCathegoryHandler
from messageprocessing.handlers.cathegorieshandler.create_cathegory_handler import CreateCathegoryHandler
from messageprocessing.handlers.commonhandlers.choose_option_handler import ChooseOptionHandler
from database.api import DatabaseApi
from database.types.cathegory import Cathegory
from .utils import cathegories_to_string


class CathegoriesMainMenuHandler(ReusableHandler):
    CHOOSE_OPTION_MESSAGE = "\n\nВыберите действие"

    CREATE_CATHEGORY_OPTION_NAME = "Создать категорию"
    CHANGE_CATHEGORY_OPTION_NAME = "Изменить категорию"
    DELETE_CATHEGORY_OPTION_NAME = "Удалить категорию"
    FINISH_OPTION_NAME = "Завершить"


    OPTIONS = [
        CREATE_CATHEGORY_OPTION_NAME,
        CHANGE_CATHEGORY_OPTION_NAME,
        DELETE_CATHEGORY_OPTION_NAME,
        FINISH_OPTION_NAME,
    ]

    CHOOSING_OPTION_STATE = 0
    OTHER_STATE = 1

    def __init__(self) -> None:
        self.income_cathegories: list[Cathegory] = []
        self.expense_cathegories: list[Cathegory] = []
        self.state = __class__.CHOOSING_OPTION_STATE

    def handle_message(self, message: Message):
        return self

    @staticmethod
    def switch_to_this_handler(message: Message):
        main_handler = CathegoriesMainMenuHandler()
        main_handler.load_data_from_database(message)
        asking_message = ""
        cathegories_str = cathegories_to_string(main_handler.income_cathegories, main_handler.expense_cathegories)
        asking_message += cathegories_str + __class__.CHOOSE_OPTION_MESSAGE
        return ChooseOptionHandler.switch_to_this_handler(message, main_handler, 
                                                          asking_message, __class__.OPTIONS,
                                                          add_cancel_option=False)
    
    def switch_to_existing_handler(self, message: Message):
        if self.state == __class__.OTHER_STATE:
            return self.other_sh(message)
        elif self.state == __class__.CHOOSING_OPTION_STATE:
            return self.choosing_option_sh(message)
    
    def other_sh(self, message: Message):
        asking_message = ""
        cathegories_str = cathegories_to_string(self.income_cathegories, self.expense_cathegories)
        asking_message += cathegories_str + __class__.CHOOSE_OPTION_MESSAGE
        prev_state = self.state
        self.state = __class__.CHOOSING_OPTION_STATE
        try:
            return ChooseOptionHandler.switch_to_this_handler(message, self, 
                                                                asking_message, __class__.OPTIONS,
                                                                add_cancel_option=False)
        except:
            self.state = prev_state
            raise
    
    def choosing_option_sh(self, message: Message):
        assert self.return_result
        option = self.return_result[1]
        try:
            prev_state = self.state
            if option == __class__.CREATE_CATHEGORY_OPTION_NAME:
                self.state = __class__.OTHER_STATE
                return CreateCathegoryHandler.switch_to_this_handler(message, self)
            elif option == __class__.CHANGE_CATHEGORY_OPTION_NAME:
                self.state = __class__.OTHER_STATE
                return ChangeCathegoryHandler.switch_to_this_handler(message, self)
        except:
            self.state = prev_state
            raise
        assert False, "This can not be reached. Incorrect option handling?"

    def load_data_from_database(self, message: Message):
        self.cathegories = DatabaseApi().get_person_all_cathegories_by_id(message.from_user.id)
        self.income_cathegories = filter(lambda x: x.cathegory_type_id == DatabaseApi().get_income_cathegory_type_id(), 
                                    self.cathegories)
        self.income_cathegories = list(self.income_cathegories)
        self.expense_cathegories = filter(lambda x: x.cathegory_type_id == DatabaseApi().get_expense_cathegory_type_id(), 
                                    self.cathegories)
        self.expense_cathegories = list(self.expense_cathegories)
