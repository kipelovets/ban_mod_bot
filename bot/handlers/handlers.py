import logging
import os

from math import ceil
from magic_filter import F

from aiogram import types, Router, Bot
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.handlers.utils import (extract_kwarg, format_from_language_keyboard, format_name, make_cb)
from bot.language import lang_by_code
from bot.data import LingvoData
from bot.handlers.utils import LingvoCallbackData, FinishCallbackData

logger = logging.getLogger(__name__)
router = Router()
SUPER_ADMIN = int(os.getenv('SUPER_ADMIN', ""))


@extract_kwarg("lingvo_data")
@router.message(Command('start'))
async def start(message: types.Message, lingvo_data: LingvoData):
    if message.from_user is None:
        logger.error("message without from_user %s", message.message_id)
        return
    logger.info("start %s", message.from_user.id)
    await message.answer(
        lingvo_data.messages.choose_from_language(format_name(message.from_user)),
        reply_markup=format_from_language_keyboard(message.from_user.id))


@extract_kwarg("lingvo_data")
@router.chat_member()
async def welcome(chat_member: types.ChatMemberUpdated, lingvo_data: LingvoData, bot: Bot):
    user = chat_member.new_chat_member.user
    logger.info("welcome %s chat %s", user.id, chat_member.chat.id)
    await bot.send_message(chat_member.chat.id,
                           lingvo_data.messages.choose_from_language(
                               format_name(user)),
                           reply_markup=format_from_language_keyboard(user.id))


@extract_kwarg("lingvo_data")
@router.callback_query(FinishCallbackData.filter())
async def finish(call: types.CallbackQuery,
                 callback_data: FinishCallbackData,
                 lingvo_data: LingvoData):
    if call.message is None:
        logger.error("callback without message %s", call.id)
        return
    user_id = callback_data.user_id
    if user_id != call.from_user.id and call.from_user.id != SUPER_ADMIN:
        logger.warning("finish %s wrong user %s", user_id, call.from_user.id)
        await call.answer(lingvo_data.messages.can_not_reply_to_foreign_message())
        return
    from_lang = lang_by_code(callback_data.from_lang)
    await call.message.edit_text(
        lingvo_data.messages.finished(from_lang),
        reply_markup=None)


@extract_kwarg("lingvo_data")
@router.callback_query(LingvoCallbackData.filter(F.from_lang.is_(None) & F.to_lang.is_(None)))
async def select_from_language(call: types.CallbackQuery,
                               callback_data: LingvoCallbackData,
                               lingvo_data: LingvoData):
    if call.message is None:
        logger.error("callback without message %s", call.id)
        return
    user_id = callback_data.user_id
    if user_id != call.from_user.id and call.from_user.id != SUPER_ADMIN:
        logger.warning("select_from_language %s wrong user %s", user_id, call.from_user.id)
        await call.answer(lingvo_data.messages.can_not_reply_to_foreign_message())
        return
    logger.info("select_from_language %s", user_id)
    await call.message.edit_text(
        lingvo_data.messages.choose_from_language(format_name(call.from_user)),
        reply_markup=format_from_language_keyboard(call.from_user.id))


@extract_kwarg("lingvo_data")
@router.callback_query(LingvoCallbackData.filter(F.to_lang.is_(None)))
async def select_language(call: types.CallbackQuery, callback_data: LingvoCallbackData,
                          lingvo_data: LingvoData):
    if call.message is None:
        logger.error("callback without message %s", call.id)
        return
    user_id = int(callback_data.user_id)
    if user_id != call.from_user.id and call.from_user.id != SUPER_ADMIN:
        logger.info("select_language %s wrong user %s", user_id, call.from_user.id)
        await call.answer(lingvo_data.messages.can_not_reply_to_foreign_message())
        return
    from_lang = lang_by_code(callback_data.from_lang)
    logger.info("select_language %s from_lang %s", user_id, from_lang)

    pairs = lingvo_data.data.get_language_pairs(from_lang)
    pairs_list = sorted(pairs)

    builder = InlineKeyboardBuilder()
    for i in range(0, ceil(len(pairs_list) / 2)):
        lang = pairs_list[i * 2]
        builder.button(text=lang, callback_data=make_cb(user_id=call.from_user.id,
                                                        from_lang=from_lang,
                                                        to_lang=lang))
        if i * 2 + 1 < len(pairs_list):
            second_lang = pairs_list[i * 2 + 1]
            builder.button(
                text=second_lang,
                callback_data=make_cb(
                    user_id=call.from_user.id,
                    from_lang=from_lang,
                    to_lang=second_lang))

    builder.adjust(2)
    builder.row(types.InlineKeyboardButton(text=lingvo_data.messages.button_back(from_lang),
                                           callback_data=make_cb(
        user_id=call.from_user.id).pack()))

    username = format_name(call.from_user)
    message = lingvo_data.messages.choose_target_language(username, from_lang)

    await call.message.edit_text(message, reply_markup=builder.as_markup())


@extract_kwarg("lingvo_data")
@router.callback_query(LingvoCallbackData.filter(~(F.from_lang.is_(None) | F.to_lang.is_(None))))
async def select_translator(call: types.CallbackQuery,
                            callback_data: LingvoCallbackData,
                            lingvo_data: LingvoData):
    if call.message is None:
        logger.error("callback without message %s", call.id)
        return
    user_id = int(callback_data.user_id)
    if user_id != call.from_user.id and call.from_user.id != SUPER_ADMIN:
        logger.warning("select_translator %s wrong user %s", user_id, call.from_user.id)
        await call.answer(lingvo_data.messages.can_not_reply_to_foreign_message())
        return
    from_lang = lang_by_code(callback_data.from_lang)
    to_lang = lang_by_code(callback_data.to_lang)
    prev_translator = callback_data.prev_translator

    translator = lingvo_data.data.find_next_translator(
        from_lang, to_lang, prev_translator)

    username = format_name(call.from_user)

    builder = InlineKeyboardBuilder()
    if None is translator:
        logger.warning("select_translator %s from_lang %s to_lang %s\
                    prev_translator %s no new found", user_id, from_lang, to_lang,
                       prev_translator)
        builder.button(text=lingvo_data.messages.button_back(from_lang),
                       callback_data=make_cb(
            call.from_user.id,
            from_lang))

        message = lingvo_data.messages.no_translators_found(username, from_lang, to_lang)
        await call.message.edit_text(message, reply_markup=builder.as_markup())
        return

    logger.info("select_translator %s from_lang %s to_lang %s prev_translator %s \
        next_translator %s", user_id, from_lang, to_lang, prev_translator, translator)
    if translator is not None:
        builder.button(text=lingvo_data.messages.button_next_translator(from_lang),
                       callback_data=make_cb(
            call.from_user.id,
            from_lang,
            to_lang,
            translator))
        builder.button(text=lingvo_data.messages.button_finish(from_lang),
                       callback_data=FinishCallbackData(user_id=user_id, 
                                                        from_lang=callback_data.from_lang))
        builder.button(text=lingvo_data.messages.button_back(from_lang),
                       callback_data=make_cb(
            call.from_user.id,
            from_lang))
        builder.adjust(1)

        message = lingvo_data.messages.next_translator(username, from_lang, to_lang, translator)
        await call.message.edit_text(message, reply_markup=builder.as_markup())
