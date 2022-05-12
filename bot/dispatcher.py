
from aiogram import Dispatcher
from .handlers import (select_language, start, echo)

def configure_dispatcher(dispatcher: Dispatcher):
    dispatcher.register_message_handler(start, commands="start")
    dispatcher.register_message_handler(echo)
    dispatcher.register_callback_query_handler(select_language)