from __future__ import annotations
from ..base_inner_hndl import ReturningResultHandler, BaseHandler, ReusableHandler
from telebot.types import Message, ReplyKeyboardRemove
from botstate import BotState


class GetNameHandler(ReturningResultHandler):

    def handle_message(self, message: Message) -> BaseHandler:
        if not message.text:
            return self
        self.outter_handler.return_result = message.text
        return self.outter_handler.switch_to_existing_handler(message)

    @staticmethod
    def switch_to_this_handler(message: Message, outter_handler: ReusableHandler, 
                               asking_message: str) -> GetNameHandler:
        BotState().bot.send_message(message.chat.id, asking_message, reply_markup=ReplyKeyboardRemove())
        return GetNameHandler(outter_handler)
