from singleton_decorator import singleton
from typing import Dict
from ..handlers.base_hndl import BaseHandler
from telebot import TeleBot


@singleton
class BotState:
    
    def __init__(self, bot: TeleBot) -> None:
        self.id_handler: Dict[int, BaseHandler] = {}
        self.bot = bot
