from messageprocessing.handlers.base_hndl import BaseHandler
from telebot.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from messageprocessing.botstate import BotState


# Using BotState.bot you can access the bot
class BasicHandler(BaseHandler):

    def handle_message(self, message: Message) -> BaseHandler:
        pass

    @staticmethod
    def switch_to_this_handler(message: Message, *params) -> BaseHandler:
        # Here is going initialization. For example show message when switching to this handler
        # Show buttons and so on. In the upper method you will handle these buttons

        # Sometimes you want to clear all the buttons from previous handler on this state
        # Pass reply_markup = ReplyKeyboardRemove() with sending message.

        return BasicHandler()
