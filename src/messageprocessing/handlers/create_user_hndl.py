from messageprocessing.handlers.base_hndl import BaseHandler
from telebot.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

from .cathegorieshandler.manage_cathegories_hndl import ManageCathegoriesHandler
from ..botstate import BotState
from .base_inner_hndl import BaseInnerHandler
from database.api import DatabaseApi
from database.types.person import Person


class _NewPerson:
    def __init__(self) -> None:
        self.name = ""
        self.balance = 0


class CreateUserHandler(BaseHandler):

    def handle_message(self, message: Message):
        pass # Nothing to do 
    
    @staticmethod
    def switch_to_this_handler(message: Message):
        handler = _StartCreatingUserHandler.switch_to_this_handler(
            message, _NewPerson()
        )
        return handler


class _StartCreatingUserHandler(BaseInnerHandler):
    GREETING_MESSAGE = "Давайте перейдем к созданию вашего нового профиля."

    def handle_message(self, message: Message):
        pass  # Nothing to do here

    @staticmethod
    def switch_to_this_handler(message: Message, new_person: _NewPerson):
        BotState().bot.send_message(
            message.chat.id, _StartCreatingUserHandler.GREETING_MESSAGE, reply_markup = ReplyKeyboardRemove()
        )

        # Here instantly swithing to another handler
        return _GetUserNameHandler.switch_to_this_handler(message, new_person)


class _GetUserNameHandler(BaseHandler):

    INVITE_MESSAGE = "Давайте с вами познакомимся. Как мне вас называть?"
    I_WILL_CALL_YOU_MESSAGE = "Я буду называть вас "

    def __init__(self, new_person: _NewPerson) -> None:
        self.new_person = new_person

    def handle_message(self, message: Message):
        if not message.text:
            return self
        name = message.text[:255]
        self.new_person.name = name
        BotState().bot.send_message(
            message.chat.id, __class__.I_WILL_CALL_YOU_MESSAGE + name
        )
        return _GetUserBalanceHandler.switch_to_this_handler(message, self.new_person)

    @staticmethod
    def switch_to_this_handler(message: Message, new_person: _NewPerson):
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = KeyboardButton(message.from_user.username)
        markup.add(item1)
        BotState().bot.send_message(message.chat.id, __class__.INVITE_MESSAGE, reply_markup=markup)
        return _GetUserNameHandler(new_person)


class _GetUserBalanceHandler(BaseHandler):

    INVITE_MESSAGE = (
        "Теперь разберемся с вашим текущим балансом. "
        "Какую сумму хотели бы иметь? Введите целое число."
    )

    ERROR_MESSAGE = "Вы ввели некорректное число. Попробуйте еще раз."

    def __init__(self, new_person: _NewPerson) -> None:
        self.new_person = new_person

    def handle_message(self, message: Message):
        if not message.text:
            return self
        try:
            balance = int(message.text[:20])
            self.new_person.balance = balance
            return _RegisterUserHandler.switch_to_this_handler(message, self.new_person)
        except ValueError:
            BotState().bot.send_message(message.chat.id, __class__.ERROR_MESSAGE)
            return self

    @staticmethod
    def switch_to_this_handler(message: Message, new_person: _NewPerson):
        # TODO: send message that invites to write balance
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        for button1, button2 in [("0", "10000"), ("20000", "30000"), ("40000", "50000")]:
            markup.add(button1, button2)
        BotState().bot.send_message(message.chat.id, __class__.INVITE_MESSAGE, reply_markup = markup)
        return _GetUserBalanceHandler(new_person)


class _RegisterUserHandler(BaseHandler):

    def handle_message(self, message: Message):
        pass # Nothing to do here

    @staticmethod
    def switch_to_this_handler(message: Message, new_person: _NewPerson):
        person = Person(
            id=message.from_user.id,
            name=new_person.name,
            balance=new_person.balance,
        )
        DatabaseApi().add_person(person)
        BotState().bot.send_message(message.chat.id, "С регистрацией успешно завершили. Предлагаю теперь настроить категории.", 
                                    reply_markup = ReplyKeyboardRemove())
        return ManageCathegoriesHandler.switch_to_this_handler(message)
