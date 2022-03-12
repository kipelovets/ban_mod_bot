import logging
import os
import sys
from telegram import (Bot, Update)
from telegram.ext import (Updater, CallbackContext,
                          CommandHandler, Filters, MessageHandler, ChatMemberHandler)
from .handlers import (start, echo, chat_member, my_member)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def main():
    token = os.getenv('TELEGRAM_TOKEN')
    if token is None:
        print("Error: token not defined")
        sys.exit(1)

    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(
        Filters.text & (~Filters.command), echo))
    dispatcher.add_handler(ChatMemberHandler(callback=chat_member,
                                             chat_member_types=ChatMemberHandler.CHAT_MEMBER))
    dispatcher.add_handler(ChatMemberHandler(callback=my_member,
                                             chat_member_types=ChatMemberHandler.MY_CHAT_MEMBER))
    updater.start_polling(
        allowed_updates=["message", "chat_member", "my_chat_member"])


if __name__ == "__main__":
    main()
