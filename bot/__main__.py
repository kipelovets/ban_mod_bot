import logging
import os
import sys

from aiogram import Bot, Dispatcher, executor, types
from .storage import load
from .dispatcher import configure_dispatcher

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def main():
    token = os.getenv('TELEGRAM_TOKEN')
    api_key = os.getenv('AIRTABLE_API_KEY')
    base_id = os.getenv('AIRTABLE_BASE_ID')
    table_name = os.getenv('AIRTABLE_TABLE_NAME')
    if token is None or api_key is None or base_id is None or table_name is None:
        print("Error: required env vars not defined")
        sys.exit(1)

    bot = Bot(token=token)
    dp = Dispatcher(bot)
    configure_dispatcher(dp)

    data = load(api_key, base_id, table_name)
    print(data)

    executor.start_polling(dp,
        allowed_updates=["message", "chat_member", "my_chat_member"])


if __name__ == "__main__":
    main()
