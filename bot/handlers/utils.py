import random
from typing import Optional, TypeVar, Callable, Any, Tuple

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from bot.language import code_by_lang, UA, RU, popular_pairs, OTHER_LANGUAGES

from_languages = [UA, RU]


class LingvoCallbackData(CallbackData, prefix="l", sep="|"):
    user_id: int
    from_lang: Optional[str]
    to_lang: Optional[str]


class FinishCallbackData(CallbackData, prefix="f", sep="|"):
    user_id: int
    from_lang: Optional[str]


class TranslatorCallbackData(CallbackData, prefix="t", sep="|"):
    user_id: int
    from_lang: str
    to_lang: str
    prev_translator: Optional[str] = None
    seed: int


def make_cb(
        user_id: int,
        from_lang: str | None = None,
        to_lang: str | None = None):
    to_lang = code_by_lang(to_lang) if to_lang is not None else ""
    from_lang = code_by_lang(from_lang) if from_lang is not None else ""
    return LingvoCallbackData(
        user_id=user_id,
        from_lang=from_lang,
        to_lang=to_lang
    )


def format_name(user: types.User) -> str:
    return user.username if user.username != "" and user.username is not None else user.full_name


def format_from_language_keyboard(user_id: int) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for lang in from_languages:
        builder.button(
            text=lang, callback_data=make_cb(user_id, from_lang=lang))
    builder.adjust(1)
    return builder.as_markup()


def make_seed() -> int:
    return random.randint(0, 99999)


def format_popular_languages_keyboard(user_id: int) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    seed = make_seed()
    for pair, languages in popular_pairs.items():
        from_lang, to_lang = languages
        builder.button(text=pair, callback_data=TranslatorCallbackData(
            user_id=user_id,
            from_lang=code_by_lang(from_lang),
            to_lang=code_by_lang(to_lang),
            seed=seed))
    builder.button(text=OTHER_LANGUAGES, callback_data=make_cb(user_id))
    builder.adjust(1)
    return builder.as_markup()


T = TypeVar('T')


def extract_kwargs(*kwarg_names: str) -> Callable[[Callable[..., T]], Callable[..., T]]:
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        def wrapper(*args: Tuple[Any], **kwargs: Any) -> T:
            for kwarg_name in kwarg_names:
                if kwarg_name in kwargs:
                    value = kwargs.pop(kwarg_name)
                    args += (value,)
            return func(*args, **kwargs)
        return wrapper
    return decorator
