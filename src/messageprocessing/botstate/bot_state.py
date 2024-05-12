from singleton_decorator import singleton
from typing import Dict
from ..handlers.base_handler import BaseHandler
from telebot import TeleBot


@singleton
class BotState:
    
    def __init__(self, bot: TeleBot) -> None:
        self.bot = bot
