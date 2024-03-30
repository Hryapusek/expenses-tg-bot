from .base_hndl import BaseHandler
from abc import ABC, abstractmethod
from telebot.types import Message


class BaseInnerHandler(BaseHandler):
    def __init__(self, outter_handler: BaseHandler) -> None:
        self.outter_handler = outter_handler

    @staticmethod
    @abstractmethod
    def switch_to_this_handler(message: Message, outter_handler: BaseHandler) -> BaseHandler:
        pass
