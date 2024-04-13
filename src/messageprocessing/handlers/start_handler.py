from messageprocessing.handlers.base_handler import BaseHandler
from telebot.types import Message
import telebot.types
from database.api import DatabaseApi
from psycopg2 import ProgrammingError

from messageprocessing.handlers.utils import InitializeWrapper
from .main_menu_handler import MainMenuHandler
from ..botstate import BotState
from .create_user_handler import CreateUserHandler
import logging


class StartHandler(BaseHandler):
    LETS_GO_BUTTON_NAME = "Вперед"

    GREETING_MESSAGE = ("Привет мой друг! Я бот созданный для "
                     "того чтобы помогать людям с их финансами. "
                     f"Нажмите на кнопку или напишите \"{LETS_GO_BUTTON_NAME}\" "
                     "чтобы перейти к настройке профиля.")

    MARKUP = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    MARKUP.add(LETS_GO_BUTTON_NAME)

    def handle_message(self, message: Message) -> BaseHandler:
        if message.text and message.text == __class__.LETS_GO_BUTTON_NAME:
            try:
                DatabaseApi().get_person_by_id(message.from_user.id)
                logging.info(f"User with id {message.from_user.id} was found in database. Next handler is unknown")
                return MainMenuHandler.switch_to_this_handler(message)

            except ProgrammingError:
                logging.info(f"User with id {message.from_user.id} was NOT found in database. CreateUerHandler is the next")
                return CreateUserHandler.switch_to_this_handler(message, InitializeWrapper(MainMenuHandler))
        BotState().bot.send_message(message.chat.id, self.GREETING_MESSAGE, reply_markup=self.MARKUP)
        return self

    @staticmethod
    def switch_to_this_handler(message: Message):
        BotState().bot.send_message(message.chat.id, __class__.GREETING_MESSAGE, reply_markup=__class__.MARKUP)
        return StartHandler()
