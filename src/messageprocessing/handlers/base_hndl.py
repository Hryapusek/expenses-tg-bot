from __future__ import annotations
from abc import ABC, abstractmethod
from telebot.types import Message

class BaseHandler(ABC):
    
    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def handle_message(self, message) -> BaseHandler:
        pass

    @staticmethod
    @abstractmethod
    def switch_to_this_handler(message: Message) -> BaseHandler:
        pass


class ReusableHandler(BaseHandler):
    @abstractmethod
    def switch_to_existing_handler(self, message: Message) -> ReusableHandler:
        """
        This will make possible to reuse handler.
        E.g. if you have handler object and want to activate it - call this method.
        """
        pass
