
from aiogram import Dispatcher

from bot.storage import TranslatorsData
from .handlers import (make_choose_translator,
                       make_select_language, select_from_language, start, echo, cb, welcome)


def configure_dispatcher(dispatcher: Dispatcher, data: TranslatorsData):
    dispatcher.register_message_handler(start, commands="translate")
    dispatcher.register_callback_query_handler(
        select_from_language, cb.filter(from_lang=[""], to_lang=[""]))

    select_language = make_select_language(data)

    dispatcher.register_callback_query_handler(
        select_language, cb.filter(to_lang=[""]))
    dispatcher.register_callback_query_handler(
        make_choose_translator(data), cb.filter())
    dispatcher.register_chat_member_handler(welcome)
