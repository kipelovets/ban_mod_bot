
from aiogram import Dispatcher

from bot.storage import TranslatorsData
from .handlers import (Handler, cb)


def configure_dispatcher(dispatcher: Dispatcher, data: TranslatorsData):
    handler = Handler(data)

    dispatcher.register_message_handler(handler.start, commands="translate")
    dispatcher.register_chat_member_handler(handler.welcome)

    dispatcher.register_callback_query_handler(
        handler.select_from_language, cb.filter(from_lang=[""], to_lang=[""]))
    dispatcher.register_callback_query_handler(
        handler.select_language, cb.filter(to_lang=[""]))
    dispatcher.register_callback_query_handler(
        handler.choose_translator, cb.filter())
