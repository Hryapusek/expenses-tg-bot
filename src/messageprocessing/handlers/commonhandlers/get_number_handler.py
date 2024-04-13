from __future__ import annotations
from ..base_inner_handler import ReturningResultHandler, BaseInnerHandler, ReusableHandler
from telebot.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from messageprocessing.botstate import BotState


class GetNumberHandler(ReturningResultHandler):

    BAD_NUMBER_MESSAGE = "Введено некорректное значение. Попробуйте снова"
    CANCEL_NAME = "Отмена"

    def __init__(self, outter_handler: ReusableHandler, asking_message: str, 
                 markup = None, is_valid = lambda x: (True, ""),
                 add_cancel_button=True) -> None:
        super().__init__(outter_handler)
        self.asking_message = asking_message
        self.is_valid = is_valid
        self.add_cancel_button = add_cancel_button
        self.markup = markup

    def handle_message(self, message: Message) -> BaseInnerHandler:
        if not message.text:
            return self
        if self.add_cancel_button and message.text == __class__.CANCEL_NAME:
            self.outter_handler.return_result = None
            return self.outter_handler.switch_to_existing_handler(message)
        try:
            value = int(message.text)
            result, err = self.is_valid(value)
            if not result:
                BotState().bot.send_message(message.chat.id, err, reply_markup=self.markup)
                BotState().bot.send_message(message.chat.id, self.asking_message, reply_markup=self.markup)
                return self
            self.outter_handler.return_result = value
            return self.outter_handler.switch_to_existing_handler(message)
        except ValueError:
            BotState().bot.send_message(__class__.BAD_NUMBER_MESSAGE, reply_markup=self.markup)
            return self

    @staticmethod
    def switch_to_this_handler(message: Message, outter_handler: ReusableHandler, 
                               asking_message: str, markup = None, 
                               is_valid = lambda x: (True, ""),
                               add_cancel_button=True) -> GetNumberHandler:
        """
            return_result:
                - None if cencel choosed
                - int Number that pred(Number) == True
        """
        if not markup:
            if not add_cancel_button:
                markup = ReplyKeyboardRemove()
            else:
                markup = ReplyKeyboardMarkup()
                markup.add(__class__.CANCEL_NAME)            
        elif add_cancel_button:
            markup.add(__class__.CANCEL_NAME)
        BotState().bot.send_message(message.chat.id, asking_message, reply_markup=markup)
        return GetNumberHandler(outter_handler, asking_message, markup, is_valid, add_cancel_button)
