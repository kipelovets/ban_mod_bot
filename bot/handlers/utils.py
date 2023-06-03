from typing import Optional
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from bot.language import code_by_lang, UA, RU

from_languages = [UA, RU]


class LingvoCallbackData(CallbackData, prefix="l", sep="|"):
    user_id: int
    from_lang: Optional[str]
    to_lang: Optional[str]
    prev_translator: Optional[str]


def make_cb(
        user_id: int,
        from_lang: str | None = None,
        to_lang: str | None = None,
        prev_translator: str | None = None):
    to_lang = code_by_lang(to_lang) if to_lang is not None else ""
    from_lang = code_by_lang(from_lang) if from_lang is not None else ""
    return LingvoCallbackData(
        user_id=user_id,
        from_lang=from_lang,
        to_lang=to_lang,
        prev_translator=prev_translator)


def format_name(user: types.User) -> str:
    return user.username if user.username != "" and user.username is not None else user.full_name


def format_from_language_keyboard(user_id: int) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for lang in from_languages:
        builder.button(
            text=lang, callback_data=make_cb(user_id, from_lang=lang))
    builder.adjust(1)
    return builder.as_markup()
