from messageprocessing.handlers.base_hndl import BaseHandler
from telebot.types import Message
from ..botstate import BotState 

class MainMenuHandler(BaseHandler):

    def handle_message(self, message: Message):
        # TODO: handle buttons and other messages that are 
        #       sent by switch_to_this_handler
        pass
    
    @staticmethod
    def switch_to_this_handler(message: Message):
        # TODO: send message that shows main menu
        return MainMenuHandler()
 
