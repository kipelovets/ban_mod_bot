
import logging
from math import ceil
from aiogram import types
from bot.handlers.utils import (format_from_language_keyboard, format_name, make_cb)
from bot.language import lang_by_code
from bot.messages import Messages
from bot.storage import TranslatorsData

logger = logging.getLogger(__name__)


class Handler:

    data: TranslatorsData
    messages: Messages

    def __init__(self, data: TranslatorsData, messages: Messages) -> None:
        self.data = data
        self.messages = messages

    async def echo(self, message: types.Message):
        logger.info("echo %s: %s", message.from_user.id, message.text)
        await message.answer(message.text)

    async def start(self, message: types.Message):
        logger.info("start %s", message.from_user.id)
        await message.answer(
            self.messages.welcome_choose_initial_language(format_name(message.from_user)),
            reply_markup=format_from_language_keyboard(message.from_user.id))

    async def welcome(self, chat_member: types.ChatMemberUpdated):
        user = chat_member.new_chat_member.user
        logger.info("welcome %s chat %s", user.id, chat_member.chat.id)
        await chat_member.bot.send_message(chat_member.chat.id,
                                           self.messages.welcome_choose_initial_language(
                                               format_name(user)),
                                           reply_markup=format_from_language_keyboard(user.id))

    async def select_from_language(self, call: types.CallbackQuery,
                                   callback_data: dict[str, int | str]):
        user_id = int(callback_data["user_id"])
        if user_id != call.from_user.id:
            logger.warning("select_from_language %s wrong user %s", user_id, call.from_user.id)
            await call.answer(self.messages.can_not_reply_to_foreign_message())
            return
        logger.info("select_from_language %s", user_id)
        await call.message.edit_text(
            self.messages.welcome_choose_initial_language(format_name(call.from_user)),
            reply_markup=format_from_language_keyboard(call.from_user.id))

    async def select_language(self, call: types.CallbackQuery, callback_data: dict[str, int | str]):
        user_id = int(callback_data["user_id"])
        if user_id != call.from_user.id:
            logger.info("select_language %s wrong user %s", user_id, call.from_user.id)
            await call.answer(self.messages.can_not_reply_to_foreign_message())
            return
        from_lang = lang_by_code(str(callback_data["from_lang"]))
        logger.info("select_language {user_id} from_lang {from_lang}")

        pairs = self.data.get_language_pairs(from_lang)
        pairs_list = sorted(pairs)

        keyboard = types.InlineKeyboardMarkup()
        for i in range(0, ceil(len(pairs_list) / 2)):
            lang = pairs_list[i * 2]
            if i * 2 + 1 < len(pairs_list):
                second_lang = pairs_list[i * 2 + 1]
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lang,
                        callback_data=make_cb(
                            call.from_user.id,
                            from_lang,
                            lang)),
                    types.InlineKeyboardButton(
                        text=second_lang,
                        callback_data=make_cb(
                            call.from_user.id,
                            from_lang,
                            second_lang)))
            else:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=lang,
                        callback_data=make_cb(
                            call.from_user.id,
                            from_lang,
                            lang)))

        keyboard.add(
            types.InlineKeyboardButton(
                text=self.messages.button_back(from_lang),
                callback_data=make_cb(
                    call.from_user.id)))

        username = format_name(call.from_user)
        message = self.messages.choose_target_language(username, from_lang)

        await call.message.edit_text(message, reply_markup=keyboard)

    async def select_translator(self, call: types.CallbackQuery, callback_data: dict[str, str]):
        user_id = int(callback_data["user_id"])
        if user_id != call.from_user.id:
            logger.warning("select_translator %s wrong user %s", user_id, call.from_user.id)
            await call.answer(self.messages.can_not_reply_to_foreign_message())
            return
        from_lang = lang_by_code(callback_data["from_lang"])
        to_lang = lang_by_code(callback_data["to_lang"])
        prev_translator = callback_data["prev_translator"]

        translator = self.data.find_next_translator(
            from_lang, to_lang, prev_translator)
        keyboard = types.InlineKeyboardMarkup()
        username = format_name(call.from_user)

        if None is translator:
            logger.warning("select_translator %s from_lang %s to_lang %s\
                        prev_translator %s no new found", user_id, from_lang, to_lang,
                           prev_translator)
            keyboard.add(
                types.InlineKeyboardButton(
                    text=self.messages.button_back(from_lang),
                    callback_data=make_cb(
                        call.from_user.id,
                        from_lang)))
            message = self.messages.no_translators_found(username, from_lang, to_lang)
            await call.message.edit_text(message, reply_markup=keyboard)
            return

        logger.info("select_translator %s from_lang %s to_lang %s prev_translator %s \
            next_translator %s", user_id, from_lang, to_lang, prev_translator, translator)
        if translator is not None:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=self.messages.button_next_translator(from_lang),
                    callback_data=make_cb(
                        call.from_user.id,
                        from_lang,
                        to_lang,
                        translator)))
            keyboard.add(
                types.InlineKeyboardButton(
                    self.messages.button_back(from_lang),
                    callback_data=make_cb(
                        call.from_user.id,
                        from_lang)))
            message = self.messages.next_translator(username, from_lang, to_lang, translator)
            await call.message.edit_text(message, reply_markup=keyboard)
