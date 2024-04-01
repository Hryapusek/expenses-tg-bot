from messageprocessing.handlers.base_hndl import BaseHandler, ReusableHandler
from telebot.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from ...botstate import BotState
from ..base_inner_hndl import BaseInnerHandler
from database.api import DatabaseApi
from database.types.person import Person
from database.types.cathegory import Cathegory

class CreateCathegoryHandler(BaseInnerHandler):

    def handle_message(self, message: Message):
        pass # Nothing to do here

    @staticmethod
    def switch_to_this_handler(message: Message, outter_handler) -> BaseHandler:
        cathegory = Cathegory()
        cathegory.person_id = message.from_user.id
        return _ChooseCathegoryTypeHandler.switch_to_this_handler(outter_handler, Cathegory())

class _ChooseCathegoryTypeHandler(BaseInnerHandler):
    CHOOSE_TYPE_MESSAGE = ("Выберите тип категории:\n"
                           "- Доходы\n"
                           "- Расходы\n")

    MARKUP = ReplyKeyboardMarkup()
    EXPENSE_BUTTON_NAME = "Расходы"
    INCOME_CATHEGORY_BUTTON_NAME = "Доходы"
    CANCEL_CATHEGORY_BUTTON_NAME = "Отменить"

    def __init__(self, outter_handler: BaseHandler, cathegory: Cathegory) -> None:
        super().__init__(outter_handler)
        self.cathegory = cathegory

    def handle_message(self, message: Message):
        if not message.text:
            BotState().bot.send_message(__class__.CHOOSE_TYPE_MESSAGE, reply_markup=__class__.MARKUP)    
            return self
        if message.text == __class__.EXPENSE_BUTTON_NAME:
            self.cathegory.cathegory_type_id = DatabaseApi().get_expense_cathegory_type_id()
            return _ChooseCathegoryNameHandler.switch_to_this_handler(message, self.outter_handler, self.cathegory)
        elif message.text == __class__.INCOME_CATHEGORY_BUTTON_NAME:
            self.cathegory.cathegory_type_id = DatabaseApi().get_income_cathegory_type_id()
            return _ChooseCathegoryNameHandler.switch_to_this_handler(message, self.outter_handler, self.cathegory)
        else:
            BotState().bot.send_message(__class__.CHOOSE_TYPE_MESSAGE, reply_markup=__class__.MARKUP)    
            return self

    @staticmethod
    def switch_to_this_handler(message: Message, outter_handler, cathegory: Cathegory):
        BotState().bot.send_message(message.chat.id, __class__.CHOOSE_OPTION_MESSAGE, reply_markup=__class__.MARKUP)
        return __class__(outter_handler, cathegory)


class _ChooseCathegoryNameHandler(BaseInnerHandler):
    CHOOSE_NAME_MESSAGE = ("Введите название категории")
    NAME_TOO_SHORT_MESSAGE = "Имя должно содержать минимум один символ"

    MARKUP = ReplyKeyboardRemove()

    def __init__(self, outter_handler: BaseHandler, cathegory: Cathegory) -> None:
        super().__init__(outter_handler)
        self.cathegory = cathegory

    def handle_message(self, message: Message):
        if not message.text:
            BotState().bot.send_message(__class__.CHOOSE_NAME_MESSAGE, reply_markup=__class__.MARKUP)    
            return self
        if len(message.text.strip()) < 1:
            BotState().bot.send_message(__class__.NAME_TOO_SHORT_MESSAGE, reply_markup=__class__.MARKUP)
            return self
        self.cathegory.name = message.text
        return _CathegoryMoneyLimitHandler.switch_to_this_handler(message, self.outter_handler, self.cathegory)


    @staticmethod
    def switch_to_this_handler(message: Message, outter_handler, cathegory: Cathegory):
        BotState().bot.send_message(message.chat.id, __class__.CHOOSE_OPTION_MESSAGE, reply_markup=__class__.MARKUP)
        return __class__(outter_handler, cathegory)
    
class _CathegoryMoneyLimitHandler(BaseInnerHandler):
    CHOOSE_NAME_MESSAGE = "Введите желаемое ограничение по сумме для данной категории"
    BAD_LIMIT_MESSAGE = "Введено некорректное значение. Попробуйте снова"

    MARKUP = ReplyKeyboardMarkup()
    MARKUP.add("0", "1000")
    MARKUP.add("5000", "10000")
    MARKUP.add("20000", "30000")

    def __init__(self, outter_handler: BaseHandler, cathegory: Cathegory) -> None:
        super().__init__(outter_handler)
        self.cathegory = cathegory

    def handle_message(self, message: Message):
        if not message.text:
            BotState().bot.send_message(__class__.CHOOSE_NAME_MESSAGE, reply_markup=__class__.MARKUP)    
            return self
        try:
            limit = int(message.text)
            if limit < 0: raise ValueError()
            self.cathegory.money_limit = limit
            return _CathegoryCurrentMoneyHandler.switch_to_this_handler(message, self.outter_handler, self.cathegory)
        except ValueError:
            BotState().bot.send_message(__class__.BAD_LIMIT_MESSAGE, reply_markup=__class__.MARKUP)
            return self

    @staticmethod
    def switch_to_this_handler(message: Message, outter_handler, cathegory: Cathegory):
        BotState().bot.send_message(message.chat.id, __class__.CHOOSE_NAME_MESSAGE, reply_markup=__class__.MARKUP)
        return __class__(outter_handler, cathegory)

class _CathegoryCurrentMoneyHandler(BaseInnerHandler):
    CHOOSE_NAME_MESSAGE = "Введите текущие затраты по данной категории"
    BAD_LIMIT_MESSAGE = "Введено некорректное значение. Попробуйте снова"

    MARKUP = ReplyKeyboardMarkup()
    MARKUP.add("0", "1000")
    MARKUP.add("5000", "10000")
    MARKUP.add("20000", "30000")

    def __init__(self, outter_handler: BaseHandler, cathegory: Cathegory) -> None:
        super().__init__(outter_handler)
        self.cathegory = cathegory

    def handle_message(self, message: Message):
        if not message.text:
            BotState().bot.send_message(__class__.CHOOSE_NAME_MESSAGE, reply_markup=__class__.MARKUP)    
            return self
        try:
            limit = int(message.text)
            if limit < 0: raise ValueError()
            self.cathegory.current_money = limit
            return _RegisterCathegoryHandler.switch_to_this_handler(message, self.outter_handler, self.cathegory)
        except ValueError:
            BotState().bot.send_message(__class__.BAD_LIMIT_MESSAGE, reply_markup=__class__.MARKUP)
            return self

    @staticmethod
    def switch_to_this_handler(message: Message, outter_handler, cathegory: Cathegory):
        BotState().bot.send_message(message.chat.id, __class__.CHOOSE_NAME_MESSAGE, reply_markup=__class__.MARKUP)
        return __class__(outter_handler, cathegory)

class _RegisterCathegoryHandler(BaseInnerHandler):
    CHOOSE_NAME_MESSAGE = "Категория успешно создана!"

    MARKUP = ReplyKeyboardRemove()

    def __init__(self, outter_handler: ReusableHandler, cathegory: Cathegory) -> None:
        super().__init__(outter_handler)
        self.cathegory = cathegory

    def handle_message(self, message: Message):
        if not self.cathegory.id:
            self.cathegory.id = DatabaseApi().add_cathegory(self.cathegory)
            self.outter_handler.cathegories.append(self.cathegory)
        return self.outter_handler.switch_to_existing_handler(message)

    @staticmethod
    def switch_to_this_handler(message: Message, outter_handler, cathegory: Cathegory):
        try:
            cathegory.id = DatabaseApi().add_cathegory(cathegory)
            outter_handler.cathegories.append(cathegory)
            BotState().bot.send_message(message.chat.id, __class__.CHOOSE_NAME_MESSAGE, reply_markup=__class__.MARKUP)
            return outter_handler.switch_to_existing_handler(message)
        except Exception:
            return __class__(outter_handler, cathegory)

