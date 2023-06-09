import logging
import os
import sys
import asyncio
from aiogram import Bot, Dispatcher
from bot.data_loader import load_lingvo_data
from bot.handlers.handlers import router
from bot.middleware import LingvoDataMiddleware
from bot.analytics import Analytics


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ALLOWED_UPDATES = ["message", "inline_query", "chat_member", "callback_query"]


async def main():
    token = os.getenv('TELEGRAM_TOKEN')
    if token is None:
        print("Error: required env var TELEGRAM_TOKEN not defined")
        sys.exit(1)

    bot = Bot(token=token)

    api_secret = os.getenv("GA_API_SECRET")
    measurement_id=os.getenv("GA_MEASUREMENT_ID")
    client_id=os.getenv("GA_CLIENT_ID")

    if api_secret is None or measurement_id is None or client_id is None:
        print("Error: required env vars for analytics not defined")
        sys.exit(1)
    analytics = Analytics(api_secret=api_secret,
                          measurement_id=measurement_id,
                          client_id=client_id)
    analytics.bot_started()

    dispatcher = Dispatcher()
    dispatcher.include_router(router)

    middleware = LingvoDataMiddleware(load_lingvo_data(), analytics)
    router.message.middleware(middleware)
    router.callback_query.middleware(middleware)
    router.chat_member.middleware(middleware)

    await dispatcher.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


if __name__ == "__main__":
    asyncio.run(main())
