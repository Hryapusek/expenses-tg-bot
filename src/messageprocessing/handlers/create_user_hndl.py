from messageprocessing.handlers.base_hndl import BaseHandler
from telebot.types import Message
from ..botstate import BotState
from .base_inner_hndl import BaseInnerHandler
from database.api import DatabaseApi
from database.types.person import Person


class _NewPerson:
    def __init__(self) -> None:
        self.name = ""
        self.balance = 0


class CreateUserHandler(BaseHandler):

    def __init__(self) -> None:
        self.new_person = _NewPerson()
        self.inner_handler: BaseHandler = None

    def handle_message(self, message: Message):
        self.inner_handler = self.inner_handler.handle_message(message)
        if self.inner_handler is None:
            # TODO: return cathegories handler
            pass
        return self

    @staticmethod
    def switch_to_this_handler(message: Message):
        handler = CreateUserHandler()
        handler.inner_handler = _StartCreatingUserHandler.switch_to_this_handler(
            message, handler
        )
        return handler


class _StartCreatingUserHandler(BaseInnerHandler):
    GREETING_MESSAGE = "Давайте перейдем к созданию вашего нового профиля."

    def handle_message(self, message: Message):
        pass  # Nothing to do here

    @staticmethod
    def switch_to_this_handler(message: Message, outter_handler: CreateUserHandler):
        BotState().bot.send_message(
            message.chat.id, _StartCreatingUserHandler.GREETING_MESSAGE
        )

        # Here instantly swithing to another handler
        return _GetUserNameHandler.switch_to_this_handler(message, outter_handler)

    pass


class _GetUserNameHandler(BaseInnerHandler):

    INVITE_MESSAGE = "Давайте с вами познакомимся. Как мне вас называть?"
    I_WILL_CALL_YOU_MESSAGE = "Я буду называть вас "

    def handle_message(self, message: Message):
        if not message.text:
            return self
        name = message.text[:255]
        self.outter_handler.new_person.name = name
        BotState().bot.send_message(
            message.chat.id, __class__.I_WILL_CALL_YOU_MESSAGE + name
        )
        return _GetUserBalanceHandler.switch_to_this_handler(message, self.outter_handler)

    @staticmethod
    def switch_to_this_handler(message: Message, outter_handler: CreateUserHandler):
        BotState().bot.send_message(message.chat.id, __class__.INVITE_MESSAGE)
        return _GetUserNameHandler(outter_handler)

    pass


class _GetUserBalanceHandler(BaseInnerHandler):

    INVITE_MESSAGE = (
        "Теперь разберемся с вашим текущим балансом. "
        "Какую сумму хотели бы иметь? Введите целое число."
    )

    ERROR_MESSAGE = "Вы ввели некорректное число. Попробуйте еще раз."

    def handle_message(self, message: Message):
        if not message.text:
            return self
        try:
            balance = int(message.text[:20])
            self.outter_handler.new_person.balance = balance
            return _RegisterUserHandler.switch_to_this_handler(message, self.outter_handler)
        except ValueError:
            BotState().bot.send_message(message.chat.id, __class__.ERROR_MESSAGE)
            return self

    @staticmethod
    def switch_to_this_handler(message: Message, outter_handler: CreateUserHandler):
        # TODO: send message that invites to write balance
        BotState().bot.send_message(message.chat.id, __class__.INVITE_MESSAGE)
        return _GetUserBalanceHandler(outter_handler)

    pass


class _RegisterUserHandler(BaseInnerHandler):

    def handle_message(self, message: Message):
        pass # Nothing to do here

    @staticmethod
    def switch_to_this_handler(message: Message, outter_handler: CreateUserHandler):
        # TODO: send message that invites to write balance
        person = Person(
            name=outter_handler.new_person.name,
            balance=outter_handler.new_person.balance,
        )
        DatabaseApi().add_person(person)
        BotState().bot.send_message(message.chat.id, "С регистрацией успешно завершили. Предлагаю теперь настроить категории.")
        return None # TODO: change me
