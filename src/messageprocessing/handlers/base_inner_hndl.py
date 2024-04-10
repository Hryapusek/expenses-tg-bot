from __future__ import annotations
from .base_hndl import BaseHandler, ReusableHandler
from abc import ABC, abstractmethod
from telebot.types import Message


class BaseInnerHandler(BaseHandler):
    def __init__(self, outter_handler: ReusableHandler) -> None:
        BaseHandler.__init__(self)
        self.outter_handler = outter_handler

    @staticmethod
    @abstractmethod
    def switch_to_this_handler(message: Message, outter_handler: ReusableHandler) -> BaseInnerHandler:
        pass

class ReturningResultHandler(BaseInnerHandler):
    """
        When switching back to the outter_handler - return result will be in
        outter_handler.return_result
    """
    def __init__(self, outter_handler: ReusableHandler) -> None:
        ReusableHandler.__init__(self)
        self.outter_handler = outter_handler
