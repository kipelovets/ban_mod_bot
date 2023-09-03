import logging
import os
from datetime import datetime

from aiogram import types, Router, Bot, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.analytics import Analytics
from bot.handlers.utils import (
    ADMIN_URL,
    RestartCallbackData,
    TranslatorCallbackData,
    extract_kwargs,
    format_finish_keyboard,
    format_from_language_keyboard,
    format_name,
    format_welcome_message_keyboard,
    make_cb,
    format_start_message_keyboard,
    make_seed)
from bot.language import DEFAULT_LANGUAGE, code_by_lang, lang_by_code, prettify_lang, languages
from bot.lingvo_data import LingvoData
from bot.handlers.utils import LingvoCallbackData, FinishCallbackData
from bot.timer import Timer

logger = logging.getLogger(__name__)
router = Router()
SUPER_ADMIN = int(os.getenv('SUPER_ADMIN', ""))
MESSAGE_REMOVE_TIMEOUT = 60 * 60


@extract_kwargs("lingvo_data", "analytics")
@router.message(Command('start'), F.chat.type.in_({"private"}))
async def start(message: types.Message,
                lingvo_data: LingvoData,
                analytics: Analytics):
    if message.from_user is None:
        logger.error("message without from_user %s", message.message_id)
        return
    logger.info("start %s", message.from_user.id)
    analytics.start(message.from_user.id)
    keyboard = format_start_message_keyboard(
        message.from_user.id,
        lingvo_data.messages.other_languages(DEFAULT_LANGUAGE),
        lingvo_data.messages.no_help_needed(DEFAULT_LANGUAGE))
    await message.answer(
        lingvo_data.messages.welcome_choose_popular_pairs(format_name(message.from_user)),
        reply_markup=keyboard)


@extract_kwargs("lingvo_data", "analytics")
@router.callback_query(RestartCallbackData.filter(), F.message.chat.type.in_({"private"}))
async def restart(call: types.CallbackQuery,
                  callback_data: RestartCallbackData,
                  lingvo_data: LingvoData,
                  analytics: Analytics):
    if call.message is None:
        logger.error("restart without message %s", call.id)
        return
    user_id = callback_data.user_id
    if user_id not in (call.from_user.id, SUPER_ADMIN):
        logger.warning("restart %s wrong user %s", user_id, call.from_user.id)
        await call.answer(lingvo_data.messages.can_not_reply_to_foreign_message())
        return
    logger.info("restart %s", call.from_user.id)
    analytics.restart(call.from_user.id)
    keyboard = format_start_message_keyboard(
        call.from_user.id,
        lingvo_data.messages.other_languages(DEFAULT_LANGUAGE),
        lingvo_data.messages.no_help_needed(DEFAULT_LANGUAGE))
    await call.message.edit_text(
        lingvo_data.messages.welcome_choose_popular_pairs(format_name(call.from_user)),
        reply_markup=keyboard)


@extract_kwargs("lingvo_data", "analytics")
@router.chat_member()
async def welcome(chat_member: types.ChatMemberUpdated,
                  lingvo_data: LingvoData,
                  bot: Bot,
                  analytics: Analytics):
    if chat_member.new_chat_member.status != 'member':
        return
    user = chat_member.new_chat_member.user
    logger.info("welcome %s chat %s", user.id, chat_member.chat.id)
    analytics.chat_member(user.id)
    text = lingvo_data.messages.welcome_to_chat(format_name(user), DEFAULT_LANGUAGE)
    keyboard = format_welcome_message_keyboard(
        lingvo_data.messages.find_text_translator(DEFAULT_LANGUAGE),
        lingvo_data.messages.find_voice_translator(DEFAULT_LANGUAGE))
    await bot.send_message(chat_member.chat.id,
                           text,
                           reply_markup=keyboard)


@extract_kwargs("lingvo_data", "analytics")
@router.callback_query(FinishCallbackData.filter())
async def finish(call: types.CallbackQuery,
                 callback_data: FinishCallbackData,
                 lingvo_data: LingvoData,
                 analytics: Analytics):
    if call.message is None:
        logger.error("finish without message %s", call.id)
        return
    user_id = callback_data.user_id
    if user_id not in (call.from_user.id, SUPER_ADMIN):
        logger.warning("finish %s wrong user %s", user_id, call.from_user.id)
        await call.answer(lingvo_data.messages.can_not_reply_to_foreign_message())
        return
    from_lang = lang_by_code(callback_data.from_lang)
    analytics.finish(user_id)
    await call.message.edit_text(
        lingvo_data.messages.finished(from_lang),
        reply_markup=format_finish_keyboard(user_id, callback_data.from_lang or "",
                                            lingvo_data.messages.restart(from_lang)))


@extract_kwargs("lingvo_data", "analytics")
@router.callback_query(LingvoCallbackData.filter(F.from_lang.is_(None) & F.to_lang.is_(None)))
async def select_from_language(call: types.CallbackQuery,
                               callback_data: LingvoCallbackData,
                               lingvo_data: LingvoData,
                               analytics: Analytics):
    if call.message is None:
        logger.error("callback without message %s", call.id)
        return
    user_id = callback_data.user_id
    if user_id not in (call.from_user.id, SUPER_ADMIN):
        logger.warning("select_from_language %s wrong user %s", user_id, call.from_user.id)
        await call.answer(lingvo_data.messages.can_not_reply_to_foreign_message())
        return
    logger.info("select_from_language %s", user_id)
    analytics.select_from_language(user_id)
    await call.message.edit_text(
        lingvo_data.messages.choose_from_language(format_name(call.from_user)),
        reply_markup=format_from_language_keyboard(call.from_user.id))


@extract_kwargs("lingvo_data", "analytics")
@router.callback_query(LingvoCallbackData.filter(F.to_lang.is_(None)))
async def select_language(call: types.CallbackQuery,
                          callback_data: LingvoCallbackData,
                          lingvo_data: LingvoData,
                          analytics: Analytics):
    if call.message is None:
        logger.error("callback without message %s", call.id)
        return
    user_id = int(callback_data.user_id)
    if user_id not in (call.from_user.id, SUPER_ADMIN):
        logger.info("select_language %s wrong user %s", user_id, call.from_user.id)
        await call.answer(lingvo_data.messages.can_not_reply_to_foreign_message())
        return
    if callback_data.from_lang is None:
        logger.error("callback without from_lang %s", call.id)
        return
    from_lang = lang_by_code(callback_data.from_lang)
    logger.info("select_language %s from_lang %s", user_id, from_lang)
    analytics.select_to_language(user_id, from_lang)

    target_languages = lingvo_data.data.available_targets(from_lang)
    seed = make_seed()

    builder = InlineKeyboardBuilder()
    for _, lang in languages.items():
        if lang in target_languages:
            builder.button(
                text=prettify_lang(lang),
                callback_data=TranslatorCallbackData(
                    user_id=call.from_user.id,
                    from_lang=callback_data.from_lang,
                    to_lang=code_by_lang(lang),
                    seed=seed))

    builder.adjust(2)
    builder.row(types.InlineKeyboardButton(text=lingvo_data.messages.button_back(from_lang),
                                           callback_data=make_cb(
        user_id=call.from_user.id).pack()))

    username = format_name(call.from_user)
    message = lingvo_data.messages.choose_target_language(username, from_lang)

    await call.message.edit_text(message, reply_markup=builder.as_markup())


@extract_kwargs("lingvo_data", "analytics", "timer")
@router.callback_query(TranslatorCallbackData.filter())
async def select_translator(call: types.CallbackQuery,
                            callback_data: TranslatorCallbackData,
                            lingvo_data: LingvoData,
                            analytics: Analytics,
                            timer: Timer):
    if call.message is None:
        logger.error("callback without message %s", call.id)
        return
    user_id = int(callback_data.user_id)
    if user_id not in (call.from_user.id, SUPER_ADMIN):
        logger.warning("select_translator %s wrong user %s", user_id, call.from_user.id)
        await call.answer(lingvo_data.messages.can_not_reply_to_foreign_message())
        return

    from_lang = lang_by_code(callback_data.from_lang)
    to_lang = lang_by_code(callback_data.to_lang)
    prev_translator = callback_data.prev_translator
    current_time = datetime.now()

    if not timer.can_send_translator_option(user_id):
        analytics.too_fast(user_id, from_lang, to_lang)
        logger.warning(
            "select_translator too fast %s (%s, %s, %s)",
            user_id,
            current_time.strftime("%X"),
            call.message.date.strftime("%X"),
            datetime.fromtimestamp(call.message.edit_date).strftime("%X")
            if call.message.edit_date is not None else "")
        await call.answer(lingvo_data.messages.next_translator_timeout(from_lang))
        return

    translator = lingvo_data.data.find_next_translator(
        from_lang, to_lang, callback_data.seed, prev_translator)

    username = format_name(call.from_user)

    builder = InlineKeyboardBuilder()
    if translator is None:
        logger.warning("select_translator %s from_lang %s to_lang %s\
                    prev_translator %s no new found", user_id, from_lang, to_lang,
                       prev_translator)
        analytics.no_translator_option(user_id, from_lang, to_lang)
        builder.button(text=lingvo_data.messages.button_back(from_lang),
                       callback_data=make_cb(
            call.from_user.id,
            from_lang))

        message = lingvo_data.messages.no_translators_found(username, from_lang, to_lang)
        await call.message.edit_text(message, reply_markup=builder.as_markup())
        return

    logger.info("select_translator %s from_lang %s to_lang %s prev_translator %s \
        next_translator %s", user_id, from_lang, to_lang, prev_translator, translator)
    analytics.translator_option(user_id, from_lang, to_lang, translator)

    builder.button(text=lingvo_data.messages.button_next_translator(from_lang),
                   callback_data=TranslatorCallbackData(
        user_id=call.from_user.id,
        from_lang=callback_data.from_lang,
        to_lang=callback_data.to_lang,
        seed=callback_data.seed,
        prev_translator=translator))
    builder.button(text=lingvo_data.messages.button_finish(from_lang),
                   callback_data=FinishCallbackData(user_id=user_id,
                                                    from_lang=callback_data.from_lang))
    builder.button(text=lingvo_data.messages.button_back(from_lang),
                   callback_data=make_cb(
        call.from_user.id,
        from_lang))
    builder.button(text=lingvo_data.messages.contact_admin(from_lang),
                   url=ADMIN_URL)
    builder.adjust(1)

    message = lingvo_data.messages.next_translator(username, from_lang, to_lang, translator)
    await call.message.edit_text(message, reply_markup=builder.as_markup())
