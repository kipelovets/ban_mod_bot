import logging
import os
import sys
import asyncio
from aiogram import Bot, Dispatcher
from bot.data_loader import load_lingvo_data
from bot.handlers.handlers import router
from bot.middleware import LingvoDataMiddleware


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ALLOWED_UPDATES = ["message", "inline_query", "chat_member", "callback_query"]


async def main():
    token = os.getenv('TELEGRAM_TOKEN')
    if token is None:
        print("Error: required env var TELEGRAM_TOKEN not defined")
        sys.exit(1)
    bot = Bot(token=token)

    dispatcher = Dispatcher()
    dispatcher.include_router(router)
    router.message.middleware(LingvoDataMiddleware(load_lingvo_data()))

    await dispatcher.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


if __name__ == "__main__":
    asyncio.run(main())
