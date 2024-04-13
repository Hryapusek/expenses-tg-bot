from __future__ import annotations
from database.api import DatabaseApi
from messageprocessing.handlers.base_inner_handler import ReturningResultHandler, ReusableHandler
from telebot.types import Message
from messageprocessing.handlers.base_handler import BaseHandler
from messageprocessing.handlers.commonhandlers.choose_option_handler import (
    ChooseOptionHandler,
)
from messageprocessing.handlers.commonhandlers.option import Option


class ChooseCathegoryTypeHandler(ReturningResultHandler, ReusableHandler):

    CHOOSE_TYPE_MESSAGE = "Выберите тип категории"

    EXPENSE_CATHEGORY_NAME = "Расходы"
    INCOME_CATHEGORY_NAME = "Доходы"

    def handle_message(self, message) -> BaseHandler:
        return self

    @staticmethod
    def switch_to_this_handler(
        message: Message, outter_handler: ReusableHandler
    ) -> ChooseCathegoryTypeHandler:
        """
        return_result:
            - cathegory_type_id
            - None if cancel option choosed
        """
        options = [
            Option(
                __class__.EXPENSE_CATHEGORY_NAME,
                DatabaseApi().get_expense_cathegory_type_id(),
            ),
            Option(
                __class__.INCOME_CATHEGORY_NAME,
                DatabaseApi().get_income_cathegory_type_id(),
            ),
        ] # It is important not to put "options" in body, because DatabaseApi may raise some shitty Exception YA KNOW DAT HUH??????
        this_handler = __class__(outter_handler)
        return ChooseOptionHandler.switch_to_this_handler(
            message,
            this_handler,
            __class__.CHOOSE_TYPE_MESSAGE,
            options,
            add_cancel_option=True,
        )
    
    def switch_to_existing_handler(self, message: Message) -> ReusableHandler:
        """
        return_result:
            - None if canceled
            - Cathegory type id otherwise
        """
        if self.return_result:
            self.outter_handler.return_result = self.return_result[1].args[0]
            return self.outter_handler.switch_to_existing_handler(message)
        
        self.outter_handler.return_result = None
        return self.outter_handler.switch_to_existing_handler(message)

