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