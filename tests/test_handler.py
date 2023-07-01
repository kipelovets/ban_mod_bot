from unittest.mock import AsyncMock, Mock, patch

from aiogram import types

import bot.handlers.handlers as handler
from bot.lingvo_data import LingvoData
from bot.handlers.utils import TranslatorCallbackData, make_cb
from bot.timer import Timer
from .utils import given_messages, given_user, \
    given_new_chat_member, given_callback_query, ID, \
    then_message_edited, then_message_sent, then_answer

WELCOME_KEYBOARD = [
    [types.InlineKeyboardButton(
        text="укр ↔ нем", callback_data='t|123|ua|de||1000')],
    [types.InlineKeyboardButton(
        text="рус ↔ нем", callback_data='t|123|ru|de||1000')],
    [types.InlineKeyboardButton(
        text="Другие языки", callback_data='l|123||')],
    [types.InlineKeyboardButton(
        text="Мне не нужна помощь", callback_data='f|123|ru')],
]

SELECT_FROM_KEYBOARD = [
    [types.InlineKeyboardButton(
        text="украинский", callback_data='l|123|ua|')],
    [types.InlineKeyboardButton(
        text="русский", callback_data='l|123|ru|')],
]


def make_lingvo_data() -> LingvoData:
    mock_data = Mock()
    mock_data.available_targets = Mock(
        return_value=['немецкий', 'английский', "грузинский"])
    mock_data.find_next_translator = Mock(return_value="translator_username")
    mock_data.find_all_languages = Mock(
        return_value={"русский", "украинский", 'немецкий', 'английский', "грузинский"})

    return LingvoData(mock_data, given_messages())


def make_analytics_mock() -> Mock:
    return Mock()


async def test_start():
    user_mock = given_user()
    message_mock = AsyncMock(from_user=user_mock)

    with patch('random.randint') as randint_mock:
        randint_mock.return_value = 1000
        await handler.start(message_mock, make_lingvo_data(), make_analytics_mock(), AsyncMock())
    then_answer(
        message_mock, "_ welcome Joss", WELCOME_KEYBOARD)


async def test_welcome():
    chat_member_mock = given_new_chat_member()
    with patch('random.randint') as randint_mock:
        randint_mock.return_value = 1000
        await handler.welcome(chat_member_mock,
                              make_lingvo_data(),
                              chat_member_mock.bot,
                              make_analytics_mock(),
                              AsyncMock())
    then_message_sent(chat_member_mock.bot, chat_member_mock.chat.id,
                      '_ welcome Joss',
                      WELCOME_KEYBOARD)


async def test_welcome_member_left():
    chat_member_mock = given_new_chat_member()
    chat_member_mock.new_chat_member.status = "left"
    await handler.welcome(chat_member_mock,
                          make_lingvo_data(),
                          chat_member_mock.bot,
                          make_analytics_mock(),
                          AsyncMock())
    chat_member_mock.bot.send_message.assert_not_called()


async def test_select_from_language():
    call = given_callback_query()
    await handler.select_from_language(call, make_cb(ID), make_lingvo_data(), make_analytics_mock())
    call.answer.assert_not_called()
    then_message_edited(call.message,
                        "Привет @Joss!\nВыберите:",
                        SELECT_FROM_KEYBOARD)


async def test_select_from_language_clicked_by_another_user():
    call = given_callback_query()
    await handler.select_from_language(call,
                                       make_cb(ID + 1),
                                       make_lingvo_data(),
                                       make_analytics_mock())
    call.answer.assert_called_once_with(
        "Вы не можете отвечать на чужое сообщение!")
    call.message.edit_text.assert_not_called()


async def test_select_language():
    call = given_callback_query()
    with patch('random.randint') as randint_mock:
        randint_mock.return_value = 1000
        await handler.select_language(call, make_cb(ID, "украинский"),
                                      make_lingvo_data(), make_analytics_mock())
    call.answer.assert_not_called()
    expected_message = """[UA] Привет @Joss!
Выбранный язык: украинский
Теперь:"""
    then_message_edited(
        call.message, expected_message, [
            [
                types.InlineKeyboardButton(text='немецкий 🇩🇪', callback_data='t|123|ua|de||1000'),
                types.InlineKeyboardButton(text='английский 🇬🇧', callback_data='t|123|ua|en||1000'),
            ],
            [
                types.InlineKeyboardButton(text="грузинский", callback_data='t|123|ua|ka||1000')
            ],
            [
                types.InlineKeyboardButton(text="Назад", callback_data="l|123||")
            ],
        ])


async def test_select_language_clicked_by_another_user():
    call = given_callback_query()
    await handler.select_language(call, make_cb(ID + 1, "украинский"),
                                  make_lingvo_data(), make_analytics_mock())
    call.answer.assert_called_once_with(
        "Вы не можете отвечать на чужое сообщение!")
    call.message.edit_text.assert_not_called()


def mock_storage():
    storage = Mock()
    storage.last_translator_option_time = Mock(return_value=None)
    return storage


async def test_select_translator():
    call = given_callback_query()
    lingvo_data = make_lingvo_data()
    await handler.select_translator(call, TranslatorCallbackData(
        user_id=ID, from_lang="ua", to_lang="de", seed=1000),
        lingvo_data, make_analytics_mock(), Timer(mock_storage()))

    expected_buttons = [
        [
            types.InlineKeyboardButton(
                text="Следующий переводчик", callback_data="t|123|ua|de|translator_username|1000"),
        ], [
            types.InlineKeyboardButton(
                text="_ button finish", callback_data="f|123|ua")], [
            types.InlineKeyboardButton(
                text="Назад", callback_data="l|123|ua|")], ]
    then_message_edited(call.message,
                        """Привет @Joss!
Следующий переводчик для пары украинский - немецкий: translator_username""",
                        expected_buttons=expected_buttons)
    call.answer.assert_not_called()
    method_mock: Mock = lingvo_data.data.find_next_translator  # type: ignore
    method_mock.assert_called_once_with(
        "украинский", 'немецкий', 1000, None)


async def test_select_translator_clicked_by_another_user():
    call = given_callback_query()
    await handler.select_translator(call, make_cb(ID + 1, "украинский", 'немецкий'),
                                    make_lingvo_data(), make_analytics_mock(),
                                    Timer(mock_storage()))
    call.answer.assert_called_once_with(
        "Вы не можете отвечать на чужое сообщение!")
    call.message.edit_text.assert_not_called()
