
from typing import Awaitable, Callable
from aiogram import Dispatcher
from .handlers import (Handler, cb)


def configure_dispatcher(dispatcher: Dispatcher, handler: Handler,
                         reloader: Callable[..., Awaitable[None]]) -> None:

    dispatcher.register_message_handler(handler.start, commands="translate")
    dispatcher.register_chat_member_handler(handler.welcome)

    dispatcher.register_callback_query_handler(
        handler.select_from_language, cb.filter(from_lang=[""], to_lang=[""]))
    dispatcher.register_callback_query_handler(
        handler.select_language, cb.filter(to_lang=[""]))
    dispatcher.register_callback_query_handler(
        handler.select_translator, cb.filter())

    dispatcher.register_message_handler(reloader, commands="reload")
