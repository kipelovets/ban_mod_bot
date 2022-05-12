
from aiogram import Dispatcher
from .handlers import (start, echo)

def configure_dispatcher(dispatcher: Dispatcher):
    dispatcher.register_message_handler(start, commands="start")
    dispatcher.register_message_handler(echo)