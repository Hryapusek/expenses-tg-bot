from messageprocessing.handlers.base_hndl import BaseHandler
from telebot.types import Message
import telebot.types
from database.api import DatabaseApi
from psycopg2 import ProgrammingError
from .main_menu_hndl import MainMenuHandler
from ..botstate import BotState
from .create_user_hndl import CreateUserHandler
import logging


class StartHandler(BaseHandler):
    hello_message = ("Привет мой друг! Я бот созданный для "
                     "того чтобы помогать людям с их финансами. "
                     "Нажмите на кнопку или напишите \"вперед\" "
                     "чтобы перейти к настройке профиля.")

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton("let's go"))

    def handle_message(self, message: Message):
        if message.text and message.text == "let's go":
            if not (message.from_user and message.from_user.id):
                return self
            
            try:
                DatabaseApi().get_person_by_id(message.from_user.id)
                logging.info(f"User with id {message.from_user.id} was found in database. Next handler is unknown")
                return MainMenuHandler.switch_to_this_handler(message)

            except ProgrammingError:
                logging.info(f"User with id {message.from_user.id} was NOT found in database. CreateUerHandler is the next")
                return CreateUserHandler.switch_to_this_handler(message)

            except Exception as e:
                logging.error("Exception while handling message in StartHandler. Exception: ", exc_info=e)
                BotState().bot.send_message(message.chat.id, "Внутренняя ошибка")
                return self
                # TODO: send internal error message and log this error
        
        BotState().bot.send_message(message.chat.id, self.hello_message, reply_markup=self.markup)
        return self

    @staticmethod
    def switch_to_this_handler(message: Message):
        return StartHandler()
