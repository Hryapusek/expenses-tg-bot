from __future__ import annotations
from ..base_inner_hndl import ReturningResultHandler, BaseHandler, ReusableHandler
from telebot.types import Message, ReplyKeyboardMarkup
from botstate import BotState


class GetTextHandler(ReturningResultHandler):

    CANCEL_NAME = "Отмена"

    def __init__(self, outter_handler: ReusableHandler, asking_message: str, 
                 markup = ReplyKeyboardMarkup(), pred = lambda x: (True, "")) -> None:
        super().__init__(outter_handler)
        self.asking_message = asking_message
        self.markup = markup
        self.pred = pred

    def handle_message(self, message: Message) -> BaseHandler:
        if not message.text:
            return self
        if message.text == __class__.CANCEL_NAME:
            self.outter_handler.return_result = None
            return self.outter_handler.switch_to_existing_handler(message)
        result, err = self.pred(message.text)
        if not result:
            BotState().bot.send_message(message.chat.id, err, reply_markup=self.markup)
            BotState().bot.send_message(message.chat.id, self.asking_message, reply_markup=self.markup)
            return self
        self.outter_handler.return_result = message.text
        return self.outter_handler.switch_to_existing_handler(message)

    @staticmethod
    def switch_to_this_handler(message: Message, outter_handler: ReusableHandler, 
                               asking_message: str, markup = ReplyKeyboardMarkup(), 
                               pred = lambda x: (True, "")) -> GetTextHandler:
        BotState().bot.send_message(message.chat.id, asking_message, reply_markup=markup)
        return GetTextHandler(outter_handler, asking_message, markup, pred)
