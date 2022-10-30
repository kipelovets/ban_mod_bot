
from math import floor
from aiogram import types
from bot.handlers.utils import (format_from_language_keyboard,
                                format_from_language_message, format_name, make_cb)
from bot.language import lang_by_code
from bot.storage import TranslatorsData


class Handler:

    data: TranslatorsData

    def __init__(self, data: TranslatorsData) -> None:
        self.data = data

    async def echo(self, message: types.Message):
        await message.answer(message.text)

    async def start(self, message: types.Message):
        await message.answer(
            format_from_language_message(format_name(message.from_user)),
            reply_markup=format_from_language_keyboard(message.from_user.id))

    async def welcome(self, chat_member: types.ChatMemberUpdated):
        user = chat_member.new_chat_member.user
        await chat_member.bot.send_message(chat_member.chat.id,
                                           format_from_language_message(
                                               format_name(user)),
                                           reply_markup=format_from_language_keyboard(user.id))

    async def select_from_language(self, call: types.CallbackQuery, callback_data: dict):
        user_id = int(callback_data["user_id"])
        if user_id != call.from_user.id:
            await call.answer("Вы не можете отвечать на чужое сообщение!")
            return
        await call.message.edit_text(format_from_language_message(format_name(call.from_user)),
                                     reply_markup=format_from_language_keyboard(call.from_user.id))

    async def select_language(self, call: types.CallbackQuery, callback_data: dict):
        user_id = int(callback_data["user_id"])
        if user_id != call.from_user.id:
            await call.answer("Вы не можете отвечать на чужое сообщение!")
            return
        from_lang = lang_by_code(callback_data["from_lang"])

        pairs = self.data.get_language_pairs(from_lang)
        pairs_list = sorted(pairs)

        keyboard = types.InlineKeyboardMarkup()
        for i in range(0, floor(len(pairs_list) / 2)):
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
                text="Назад",
                callback_data=make_cb(
                    call.from_user.id)))

        message = f"""Привет @{format_name(call.from_user)}!
Выбранный язык документа: {from_lang}
Теперь выберите язык на который нужно перевести:"""

        await call.message.edit_text(message, reply_markup=keyboard)

    async def choose_translator(self, call: types.CallbackQuery, callback_data: dict):
        user_id = int(callback_data["user_id"])
        if user_id != call.from_user.id:
            await call.answer("Вы не можете отвечать на чужое сообщение!")
            return
        from_lang = lang_by_code(callback_data["from_lang"])
        to_lang = lang_by_code(callback_data["to_lang"])
        prev_translator = callback_data["prev_translator"]

        translator = self.data.find_next_translator(
            from_lang, to_lang, prev_translator)
        keyboard = types.InlineKeyboardMarkup()
        if None is translator:
            keyboard.add(
                types.InlineKeyboardButton(
                    text="Назад",
                    callback_data=make_cb(
                        call.from_user.id,
                        from_lang)))
            message = f"""Привет @{format_name(call.from_user)}!
            К сожалению у нас нет переводчиков для пары {from_lang} - {to_lang}"""
            await call.message.edit_text(message, reply_markup=keyboard)
            return

        keyboard.add(
            types.InlineKeyboardButton(
                text="Следующий переводчик",
                callback_data=make_cb(
                    call.from_user.id,
                    from_lang,
                    to_lang,
                    translator)))
        keyboard.add(
            types.InlineKeyboardButton(
                "Назад",
                callback_data=make_cb(
                    call.from_user.id,
                    from_lang)))
        message = f"""Привет @{format_name(call.from_user)}!
        Следующий переводчик для пары {from_lang} - {to_lang}: {translator}"""
        await call.message.edit_text(message, reply_markup=keyboard)
