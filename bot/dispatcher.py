
from aiogram import Dispatcher

from bot.storage import TranslatorsData
from .handlers import (make_choose_translator,
                       make_select_language, select_from_language, start, echo, cb)


def configure_dispatcher(dispatcher: Dispatcher, data: TranslatorsData):
    dispatcher.register_message_handler(start, commands="start")
    dispatcher.register_message_handler(echo)
    dispatcher.register_callback_query_handler(
        select_from_language, cb.filter(from_lang=[""], to_lang=[""]))
    dispatcher.register_callback_query_handler(
        make_select_language(data), cb.filter(to_lang=[""]))
    dispatcher.register_callback_query_handler(
        make_choose_translator(data), cb.filter())
