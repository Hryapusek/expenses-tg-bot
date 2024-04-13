from telebot.types import Message
from messageprocessing.handlers.base_handler import BaseHandler, ReusableHandler


class InitializeWrapper:
    """
        switch_to_existing_handler will be replaced with call 
        switch_to_this_handler(message, *self.args, *self.kwargs)
    """
    def __init__(self, handler_class: type, *args, **kwargs) -> None:
        self.handler_class = handler_class
        self.args = args
        self.kwargs = kwargs

    def switch_to_existing_handler(self, message: Message) -> ReusableHandler:
        return self.handler_class.switch_to_this_handler(message, *self.args, *self.kwargs)
