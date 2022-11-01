from aiogram import types
from aiogram.utils.callback_data import CallbackData

from bot.language import code_by_lang

from_languages = ["украинский", "русский"]
cb = CallbackData("l", "user_id", "from_lang",
                  "to_lang", "prev_translator", sep="|")


def make_cb(user_id: int, from_lang: str = "", to_lang: str = "", prev_translator: str = ""):
    to_lang = code_by_lang(to_lang) if to_lang != "" else ""
    from_lang = code_by_lang(from_lang) if from_lang != "" else ""
    return cb.new(
        user_id=user_id,
        from_lang=from_lang,
        to_lang=to_lang,
        prev_translator=prev_translator)


def format_name(user: types.User) -> str:
    return user.username if user.username != "" and user.username is not None else user.full_name


def format_from_language_keyboard(user_id: int) -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    for lang in from_languages:
        keyboard.add(types.InlineKeyboardButton(
            text=lang, callback_data=make_cb(user_id, lang)))
    return keyboard
