from singleton_decorator import singleton
from telebot.types import Message
from ..handlers.start_handler import StartHandler
from ..handlers.base_handler import BaseHandler


@singleton
class MessageRouter:

    def __init__(self) -> None:
        self.id_handler: dict[int, BaseHandler] = {}

    def process_message(self, message: Message):
        # FIXME: add try except
        if not message.from_user:
            return

        if not message.from_user.id in self.id_handler:
            self.id_handler[message.from_user.id] = StartHandler.switch_to_this_handler(message)
            return
            
        handler = self.id_handler[message.from_user.id]
        self.id_handler[message.from_user.id] = handler.handle_message(message)
