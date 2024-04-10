from logging_setup import logging_setup
from configreader import ConfigReader
import logging
import telebot
from messageprocessing.router.message_router import MessageRouter
from messageprocessing.botstate import BotState

def main():
    logging_setup()
    logging.info("Hello world!")
    bot = telebot.TeleBot(ConfigReader().bot_token)
    BotState(bot)
    bot.register_message_handler(MessageRouter().process_message, func = lambda x: True)
    bot.polling()


if __name__ == "__main__":
    main()
