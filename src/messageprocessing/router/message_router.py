from singleton_decorator import singleton
from telebot.types import Message
from ..handlers.start_hndl import StartHandler
from ..handlers.base_hndl import BaseHandler
from typing import Dict


@singleton
class MessageRouter:

    def __init__(self) -> None:
        self.id_handler: Dict[int, BaseHandler] = {}

    def process_message(self, message: Message):
        if not message.from_user:
            return
        if not message.from_user.id in self.id_handler:
            self.id_handler[message.from_user.id] = StartHandler()
            
        handler = self.id_handler[message.from_user.id]
        self.id_handler[message.from_user.id] = handler.handle_message(message)
