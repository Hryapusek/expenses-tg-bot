from __future__ import annotations
from ..base_inner_hndl import ReturningResultHandler, BaseHandler, ReusableHandler
from telebot.types import Message, ReplyKeyboardMarkup
from botstate import BotState
from .option import Option


class ChooseOptionHandler(ReturningResultHandler):

    CANCEL_NAME = "Отмена"

    def __init__(self, outter_handler: ReusableHandler, asking_message: str, 
                 options: list[Option], markup, add_cancel = True) -> None:
        super().__init__(outter_handler)
        self.asking_message = asking_message
        self.options = options
        self.markup = markup
        self.add_cancel = add_cancel
        if add_cancel:
            markup.add(__class__.CANCEL_NAME)

    def handle_message(self, message: Message) -> BaseHandler:
        if not message.text:
            return self
        if self.add_cancel and message.text == __class__.CANCEL_NAME:
            self.outter_handler.return_result = None
            return self.outter_handler.switch_to_existing_handler(message)
        if not (message.text in self.options):
            BotState().bot.send_message(message.chat.id, self.asking_message, reply_markup=self.markup)
            return self
        self.outter_handler.return_result = self.options.index(message.text)
        return self.outter_handler.switch_to_existing_handler(message)

    @staticmethod
    def switch_to_this_handler(message: Message, outter_handler: ReusableHandler, 
                               asking_message: str, options: list[Option], add_cancel = True) -> ChooseOptionHandler:
        markup = ReplyKeyboardMarkup()
        asking_message += '\n'
        for option in options:
            asking_message += f"- {option}\n"
            markup.add(option) # TODO: finish this handler

        BotState().bot.send_message(message.chat.id, asking_message, reply_markup=markup)
        return ChooseOptionHandler(outter_handler, asking_message, options, markup, add_cancel)
