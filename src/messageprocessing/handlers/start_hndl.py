from messageprocessing.handlers.base_hndl import BaseHandler
from telebot.types import Message
import telebot.types
from database.api import DatabaseApi
from psycopg2 import ProgrammingError
from .main_menu_hndl import MainMenuHandler
from ..botstate import BotState


class StartHandler(BaseHandler):
    hello_message = ("Hello my friend! I am the bot created to "
                     "help people with their money handling. "
                     "Click the button or type \"let's go\" to "
                     "start configuring your profie.")

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton("let's go"))

    def handle_message(self, message: Message):
        if message.text and message.text == "let's go":
            if not (message.from_user and message.from_user.id):
                return self
            
            try:
                DatabaseApi().get_person_by_id(message.from_user.id)
                return MainMenuHandler.switch_to_this_handler(message)
            except ProgrammingError:
                # TODO: switch to create user handler
                pass
            except Exception:
                # TODO: send internal error message and log this error
                pass
        
        BotState().bot.send_message(message.chat.id, self.hello_message, reply_markup=self.markup)
        return self

    @staticmethod
    def switch_to_this_handler(message: Message):
        return StartHandler()
